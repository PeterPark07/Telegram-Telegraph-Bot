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
    # Handle the /help command
    response = "The following commands are available:\n\n"
    response+= "/start\n"
    response+= "/create_account\n"
    response+= "/my_account\n"
    response+= "/get_access_token\n"
    response+= "/get_page_list\n"
    response+= "/revoke_access_token\n"
    response+= "/create_page\n"
    bot.reply_to(message, response)
    
        

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
        
    elif len(input) == 4:
        response = create_account(input[1], input[2], input[3])
        bot.reply_to(message, response)
        account0 = True
    else:
        bot.reply_to(message, "Usage - /create_account <short_name> <author_name(optional)> <author_url (optional)>")
        
@bot.message_handler(func=lambda message: message.text.startswith('/login_'))
def handle_existing_account(message):
    token = message.text.split("_")[1].strip()
    try:
        result = login(token)
        global account0
        account0 = True
    except:
        result = "Invalid access token provided"
    bot.reply_to(message, result)


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



@bot.message_handler(commands=['create_page'])
def handle_page_creation(message):
    if account0:
        try:
            input = message.text.split('[')
            title = input[0].split()[1]
            input = input[1].split(']')
            content = f"<p> {input[0]} </p>"

            if input[1] != '':
                print("here we are again")
                author_info = input[1].split()
                if len(author_info) == 1:
                    response = create_page(title, content, author_info[0])
                elif len(author_info) == 2:
                    response = create_page(title, content, author_info[0], author_info[1])
                else:
                    response = "Usage - /create_page <title> <[content]> <author_name(optional)> <author_url(optional)>"
            else:
                print("here we were again")
                response = create_page(title, content)
                        
        except:
            response = "error , try Usage - /create_page <title> <[content]> <author_name(optional)> <author_url(optional)>"
    else:
        response = "Not logged in."
    
    bot.reply_to(message, response)
    
@bot.message_handler(func=lambda message: message.text.startswith('/edit_page_'))
def handle_page_edit(message):
    if account0:
        try:
            input = message.text.split()
            path = input[0].split('_')[2]
            title = input[1]
            input = message.text.split('[')[1].split(']')
            content = f"<p> {input[0]} </p>"
            
            if input[1] != '':
                
                author_info = input[1].split()
                if len(author_info) == 1:
                    response = edit_page(path, title, content, author_info[0])
                elif len(author_info) == 2:
                    response = edit_page(path, title, content, author_info[0], author_info[1])
                else:
                    response = "Usage - /edit_page_<path> <new_title> <[new_content]> <new_author_name(optional)> <new_author_url(optional)>"
            else:
                response = edit_page(path, title, content)
    
        except:
            response = "Usage - /edit_page_<path> <new_title> <[new_content]> <new_author_name(optional)> <new_author_url(optional)>"
    else:
        response = "Not logged in."
    
    bot.reply_to(message, response)
    
    
@bot.message_handler(func=lambda message: message.text.startswith('/get_page_'))
def handle_page(message):
    if account0:
        try:
            path = message.text.split()[0].split('_')[2]
            result = get_page(path)
        except:
            result == 'Page not found'
    else:
        result =  "Not logged in."
    
    bot.reply_to(message, result)
    