import random
from datetime import datetime,timedelta
from telegram.ext import Dispatcher,CommandHandler
from telegram import BotCommand
import config

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

coins = config.CONFIG["coins"]

def check_user(chatid,user):
    uid = str(user.id)
    first_name = user.first_name
    if not chatid in coins.keys():
        coins[chatid] = {}
    if not uid in coins[chatid].keys():
        coins[chatid][uid] = {'name':first_name,'coins':0,'count':0,'dailytime':'2002/02/02 00:00:00'}

def get_dailytime(chatid,uid):
    return datetime.strptime(coins[chatid][uid]['dailytime'],'%Y/%m/%d %H:%M:%S')

def set_dailytime(chatid,uid,time):
    coins[chatid][uid]['dailytime']=time.strftime('%Y/%m/%d %H:%M:%S')
    
def save():
    config.CONFIG["coins"] = coins
    config.save_config()

def show_user(chatid,user):
    uid = str(user.id)
    check_user(chatid,user)
    #  老房东(10):200
    return f"{coins[chatid][uid]['name']}({coins[chatid][uid]['count']}):{coins[chatid][uid]['coins']}"

def add_coins(chatid,user,c):
    check_user(chatid,user)
    chatid = str(chatid)
    uid = str(user.id)
    coins[chatid][uid]['coins'] += c
    save()

def add_count(chatid,user):
    chatid = str(chatid)
    check_user(chatid,user)
    uid = str(user.id)
    coins[chatid][uid]['count'] += 1
    config.CONFIG["coins"] = coins
    config.save_config()

def daily(chatid,user):
    chatid = str(chatid)
    check_user(chatid,user)
    uid = str(user.id)
    if datetime.now() > get_dailytime(chatid,uid):
        c = random.randint(1,100)
        coins[chatid][uid]['coins'] += c
        set_dailytime(chatid,uid,datetime.now() + timedelta(minutes=5))
        save()
        return c
    else:
        return 0

def get_coins(update, context):
    chatid = str(update.effective_chat.id)
    user = update.effective_user
    check_user(chatid,user)
    # update.message.reply_text(f"{show_user(chatid,user)}")
    update.message.reply_animation('https://5b0988e595225.cdn.sohucs.com/images/20190320/8fd8429c05784afebc378c04f1ac8005.gif',caption=f"{show_user(chatid,user)}")

def add_handler(dp:Dispatcher):
    dp.add_handler(CommandHandler('coins', get_coins))

def get_command():
    return [BotCommand('coins','看看你的金币有没有丢失')]