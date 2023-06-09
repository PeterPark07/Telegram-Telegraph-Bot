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
    bot.reply_to(message, "use /start, /create_account , /my_account, /get_access_token, /get_page_list, /revoke_access_token")
    
        
@bot.message_handler(commands=['login_'])
def handle_existing_account(message):
    token = message.text.split("_")[1].strip()
    try:
        result = login(token)
    except:
        result = "Invalid access token provided"
    bot.reply_to(message, result)


@bot.message_handler(commands=['create_account'])
def handle_account_creation(message):
    global account0
    input = message.text.split()
    
    if len(input) == 2:
        response = create_account(input[1])
        bot.reply_to(message, response)
        account0 = True
        
    elif len(input) == 3:
        response = create_account(input[1], input[2])
        bot.reply_to(message, response)
        account0 = True
    else:
        bot.reply_to(message, "Usage - /create_account <short_name> <author_name(optional)>")
        
    
@bot.message_handler(commands=['my_account'])
def handle_account_info(message):
    # Handle the /start command
    if account0:
        result = get_account_info()
    else:
        result = "Not logged in."
    bot.reply_to(message, result)
    
    
@bot.message_handler(commands=['get_access_token'])
def handle_access_token(message):
    if account0:
        result = get_access_token()
    else:
        result = "Not logged in."
    bot.reply_to(message, result)

    
@bot.message_handler(commands=['get_page_list'])
def handle_page_list(message):
    if account0:
        result = get_page_list()
        if result == '':
            result = "No pages found."
    else:
        result =  "Not logged in."
    
    bot.reply_to(message, result)
    
    
@bot.message_handler(commands=['revoke_access_token'])
def handle_revoke_token(message):
    if account0:
        result = revoke_access_token()
    else:
        result = "Not logged in."
    bot.reply_to(message, result)
