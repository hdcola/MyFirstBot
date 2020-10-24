from telegram.ext import Dispatcher,CommandHandler,CallbackQueryHandler
from telegram import InlineKeyboardMarkup,InlineKeyboardButton
import random

def getNumber():
    endNumber = 0
    msg = ""
    for i in range(3):
        rnumber = random.randint(1,6)
        endNumber += rnumber
        msg += "%s "%rnumber 
    msg += "=%s" % endNumber     
    return [endNumber,msg]

def guess(update, context):
    bigButton = InlineKeyboardButton('小',callback_data='small')
    smallButton = InlineKeyboardButton('大',callback_data='big')

    kb = InlineKeyboardMarkup([[bigButton],[smallButton]])

    update.message.reply_text("请选择大或小",reply_markup=kb)

def buttonCallback(update, context):
    query = update.callback_query
    win = False
    number,msg=getNumber()   
    if query.data == 'big':
        if number >= 11:
            win = True
    elif query.data == 'small':
        if number <= 10:
            win = True
    print(number)
    if win == True:
        query.answer("%s\n恭喜你,你答对了"%msg,show_alert=True)
    else:
        query.answer("%s\n你好惨,完全错了"%msg,show_alert=True)

def add_handler(dp:Dispatcher):
    guess_handler = CommandHandler('hdguess', guess)
    dp.add_handler(guess_handler)
    dp.add_handler(CallbackQueryHandler(buttonCallback))