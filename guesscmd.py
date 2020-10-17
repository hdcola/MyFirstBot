from telegram.ext import Dispatcher,CommandHandler,CallbackQueryHandler
from telegram import InlineKeyboardMarkup,InlineKeyboardButton
import random

# rnumber = random.randint(1,99)
"""
{
    chatid:
        rnumber: 12,
        member:{
        '老房东': 2,'sicheng':1
        },
}
"""
games = {}

def help():
    return "你需要猜一个数字，它是1-99里的。"

def guess(update, context):
    chatid = update.message.chat.id
    if not (chatid in games):
        games[chatid] = { 'rnumber':random.randint(1,99), 'member':{} }
    print(games)

    bigButton = InlineKeyboardButton('大',callback_data='big')
    smallButton = InlineKeyboardButton('小',callback_data='small')
    okButton = InlineKeyboardButton('确认',callback_data='ok')
    nullButton = InlineKeyboardButton('无聊',callback_data='null')

    kb = InlineKeyboardMarkup([[bigButton],[smallButton],[okButton,nullButton]])

    if len(context.args) == 0:
        update.message.reply_text(help(),reply_markup=kb)
    else:
        if context.args[0].isdigit():
            number = int(context.args[0])
            fname = update.message.from_user.first_name
            if fname in games[chatid]['member']:
                games[chatid]['member'][fname] += 1
            else:
                games[chatid]['member'][fname] = 1
            if number == games[chatid]['rnumber']:
                update.message.reply_text("你输入的是 %s 系统随机的是 %s 你猜中了！\n 新的随机数字生成了！"%(number,games[chatid]['rnumber']),reply_markup=kb)
                games[chatid]['rnumber'] = random.randint(1,99)
                games[chatid]['member']={}
            elif number < games[chatid]['rnumber']:
                update.message.reply_text("你输入的是 %s 系统随机的是 %s 你猜小了！\n %s"%(number,games[chatid]['rnumber'],games[chatid]['rnumber']),reply_markup=kb)
            elif number > games[chatid]['rnumber']:
                update.message.reply_text("你输入的是 %s 系统随机的是 %s 你猜大了！\n %s"%(number,games[chatid]['rnumber'],games[chatid]['rnumber']),reply_markup=kb)
        else: 
            update.message.reply_text("你输入的%s不是数字"%context.args[0],reply_markup=kb)

def buttonCallback(update, context):
    query = update.callback_query
    query.answer("%s点了%s"%(update.effective_user.first_name,query.data),show_alert=True)

def add_handler(dp:Dispatcher):
    guess_handler = CommandHandler('guess', guess)
    dp.add_handler(guess_handler)
    dp.add_handler(CallbackQueryHandler(buttonCallback))

