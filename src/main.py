import os
from flask import Flask, request
from helper.func import *
import telebot

app = Flask(__name__)
bot = telebot.TeleBot(os.getenv('telegraph_bot'), threaded=False)
admin_user = int(os.getenv('admin'))
users = [int(id) for id in (os.getenv('users').split(','))]
account0 = False


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
    # Handle the /start command
    bot.reply_to(message, "Hello there! I am Telegraph Bot. Type /help for help")
    
@bot.message_handler(commands=['help'])
def handle_help(message):
    # Handle the /start command
    bot.reply_to(message, "use /start, /create_account , /my_account, /get_access_token, get_page_list")
    

@bot.message_handler(commands=['create_account'])
def handle_account_creation(message):
    global account0
    # Handle the /start command
    input = message.text
    
    input = input.split()
    
    if len(input) == 2:
        account = create_account(input[1])
        response = 'short_name - ' + account.get('short_name') + '\naccess_token - ' + account.get('access_token') + '\nauth_url - ' + account.get('auth_url')
        bot.reply_to(message, response)
        account0 = True
        
    elif len(input) == 3:
        account = create_account(input[1], input[2])
        response = 'short_name - ' + account.get('short_name') + '\nauthor_name - ' + account.get('author_name') + '\naccess_token - ' + account.get('access_token') + '\nauth_url - ' + account.get('auth_url')
        bot.reply_to(message, response)
        account0 = True
    else:
        bot.reply_to(message, "Usage - /create_account <short_name> <author_name(optional)>")
    
@bot.message_handler(commands=['my_account'])
def handle_account_info(message):
    # Handle the /start command
    if account0:
        info = get_account_info()
        result = ''
        for i in info:
            result += f"{i} -> {info.get(i)}\n"
    else:
        result = "Not logged in."
    bot.reply_to(message, result)
    
    
@bot.message_handler(commands=['get_access_token'])
def handle_access_token(message):
    if account0:
        result = get_access_token()
        result+= f"To login using this token, use /login_{result}"
    else:
        result = "Not logged in."
    bot.reply_to(message, result)
    
    
@bot.message_handler(commands=['get_page_list'])
def handle_page_list(message):
    if account0:
        result = get_page_list()
        result+= f"To login using this token, use /login_{result}"
    else:
        result = "Not logged in."
    bot.reply_to(message, result)