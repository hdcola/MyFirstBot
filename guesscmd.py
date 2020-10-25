from telegram.ext import Dispatcher,CommandHandler,CallbackQueryHandler
from telegram import InlineKeyboardMarkup,InlineKeyboardButton
import random

smallButton = InlineKeyboardButton('小',callback_data='small')
bigButton = InlineKeyboardButton('大',callback_data='big')
sumButton = InlineKeyboardButton('结算',callback_data='sum')

gamekb = InlineKeyboardMarkup([[bigButton,smallButton,sumButton]])

joinButton = InlineKeyboardButton('加入',callback_data='join')
startButton = InlineKeyboardButton('开始',callback_data='start')

startkb = InlineKeyboardMarkup([[joinButton,startButton]])


# { first_name:d, first_name:x}
games = {}

def getNumber():
    endNumber = 0
    msg = ""
    for _i in range(3):
        rnumber = random.randint(1,6)
        endNumber += rnumber
        msg += "%s "%rnumber
    msg += "=%s" % endNumber
    return [endNumber,msg]

def sumGame():
    number,msg = getNumber()
    game = 'x'
    if number >= 11:
        game = 'd'
    for u in games.keys():
        if games[u] == '':
            games[u] = '没选'
        elif games[u] == game:
            games[u] = 'Yes!'
        else:
            games[u] = 'Noo!'
    msg += "\n%s"%getUsers()
    return msg 

def getUsers():
    msg = ""
    for u in games.keys():
        msg += "%s:%s\n"%(u,games[u])
    return msg

def guess(update, context):
    update.message.reply_text("请选择大或小",reply_markup=startkb)

def buttonCallback(update, context):
    global games
    query = update.callback_query 
    if query.data == 'join':
        query.answer("加入游戏")
        games[update.effective_user.first_name] = ""
        query.edit_message_text(getUsers(),reply_markup=startkb)
        return
    elif query.data == 'start':
        query.answer("开始")
        query.edit_message_text(getUsers(),reply_markup=gamekb)
    elif query.data == 'big':
        query.answer("你选择了大")
        games[update.effective_user.first_name] = "d"
        query.edit_message_text(getUsers(),reply_markup=gamekb)
    elif query.data == 'small':
        query.answer("你选择了小")
        games[update.effective_user.first_name] = "x"
        query.edit_message_text(getUsers(),reply_markup=gamekb)
    elif query.data == 'sum':
        query.answer("结算开始")
        query.edit_message_text(sumGame())
        games = {}

def add_handler(dp:Dispatcher):
    guess_handler = CommandHandler('guess', guess)
    dp.add_handler(guess_handler)
    dp.add_handler(CallbackQueryHandler(buttonCallback))