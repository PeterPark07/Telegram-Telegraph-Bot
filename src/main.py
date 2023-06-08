import os
from flask import Flask, request
from helper.func import *
import telebot

app = Flask(__name__)
bot = telebot.TeleBot(os.getenv('telegraph_bot'), threaded=False)
bot.set_webhook(url = os.getenv('url')
state = False
admin_user = int(os.getenv('admin'))
users = [int(id) for id in (os.getenv('users').split(','))]

@app.route('/', methods=['POST'])
def telegram():
    # Process incoming updates
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200


@bot.message_handler(commands=['start'])
def handle_start(message):
    send_log(bot, message)
    # Handle the /start command
    bot.reply_to(message, "Hello there! I am Telegraph Bot. Type /help for help")