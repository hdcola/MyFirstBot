import random
from datetime import datetime,timedelta
from telegram.ext import Dispatcher,CommandHandler
from telegram import BotCommand

# {
#     chatid: {
#         uid :{
#             'name': first_name,
#             'coins': 123,
#             'count': 0,
#             'dailytime' : time
#         }
#     }
# }

coins = {}

def check_user(chatid,user):
    uid = user.id
    first_name = user.first_name
    if not chatid in coins.keys():
        coins[chatid] = {}
    if not uid in coins[chatid].keys():
        coins[chatid][uid] = {'name':first_name,'coins':0,'count':0,'dailytime':datetime.now()}

def show_user(chatid,user):
    uid = user.id
    check_user(chatid,user)
    #  老房东(10):200
    return f"{coins[chatid][uid]['name']}({coins[chatid][uid]['count']}):{coins[chatid][uid]['coins']}"

def add_coins(chatid,user,c):
    check_user(chatid,user)
    uid = user.id
    coins[chatid][uid]['coins'] += c

def add_count(chatid,user):
    check_user(chatid,user)
    uid = user.id
    coins[chatid][uid]['count'] += 1

def daily(chatid,user):
    check_user(chatid,user)
    uid = user.id
    if datetime.now() > coins[chatid][uid]['dailytime']:
        c = random.randint(1,100)
        coins[chatid][uid]['coins'] += c
        coins[chatid][uid]['dailytime'] = datetime.now() + timedelta(minutes=5)
        return c
    else:
        return 0

def get_coins(update, context):
    chatid = update.effective_chat.id
    user = update.effective_user
    check_user(chatid,user)
    update.message.reply_text(f"{show_user(chatid,user)}")

def add_handler(dp:Dispatcher):
    dp.add_handler(CommandHandler('coins', get_coins))

def get_command():
    return [BotCommand('coins','看看你的金币有没有丢失')]