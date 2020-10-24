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
    smallButton = InlineKeyboardButton('小',callback_data='small')
    bigButton = InlineKeyboardButton('大',callback_data='big')

    kb = InlineKeyboardMarkup([[bigButton,smallButton]])

    update.message.reply_text("请选择大或小",reply_markup=kb)

def buttonCallback(update, context):
    query = update.callback_query
    win = False 
    number,msg=getNumber()
    if query.data == 'big':
        msg += "\n你选择了大"
        if number >= 11:
            win = True
    elif query.data == 'small':
        msg += "\n你选择了小"
        if number <= 10:
            win = True
    print(number)
    if win == True:
        msg += "\n你答对了!"
    else:
        msg += "\n你错了！"
    query.answer("%s\n你好惨,完全错了"%msg)
    query.edit_message_text(msg)

def add_handler(dp:Dispatcher):
    guess_handler = CommandHandler('hdguess', guess)
    dp.add_handler(guess_handler)
    dp.add_handler(CallbackQueryHandler(buttonCallback))