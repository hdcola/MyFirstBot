from telegram.ext import Dispatcher,CommandHandler,CallbackQueryHandler
from telegram import InlineKeyboardMarkup,InlineKeyboardButton
import random
from datetime import datetime,timedelta

smallButton = InlineKeyboardButton('小',callback_data='small')
bigButton = InlineKeyboardButton('大',callback_data='big')
sumButton = InlineKeyboardButton('结算',callback_data='sum')

gamekb = InlineKeyboardMarkup([[bigButton,smallButton,sumButton]])

joinButton = InlineKeyboardButton('加入',callback_data='join')
startButton = InlineKeyboardButton('开始',callback_data='start')

startkb = InlineKeyboardMarkup([[joinButton,startButton]])

timer = 0

# { 
#  chatid: {
#    h:"", 
#    p:{first_name:d, first_name:x}
# }}
games = {}

def check_chatid(chatid):
    if not chatid in games.keys():
        games[chatid]={
            "h":"",
            "p":{}
            }

def getNumber():
    endNumber = 0
    msg = ""
    for _i in range(3):
        rnumber = random.randint(1,6)
        endNumber += rnumber
        msg += "%s "%rnumber
    msg += "=%s" % endNumber
    return [endNumber,msg]

def sumGame(chatid):
    number,msg = getNumber()
    game = 'x'
    users = games[chatid]["p"]
    if number >= 11:
        game = 'd'
    for u in users.keys():
        if users[u] == '':
            users[u] = '没选'
        elif users[u] == game:
            users[u] = 'Yes!'
        else:
            users[u] = 'Noo!'
    msg += "\n%s"%getUsers(users)
    return msg 

def getUsers(users):
    msg = ""
    for u in users.keys():
        msg += "%s:%s\n"%(u,users[u])
    return msg

def guess(update, context):
    global timer
    chatid = update.effective_chat.id
    check_chatid(chatid)
    timer = datetime.now() + timedelta(seconds=5)
    update.message.reply_text("请选择大或小",reply_markup=startkb)

def buttonCallback(update, context):
    global games,timer
    query = update.callback_query 
    chatid = update.effective_chat.id
    check_chatid(chatid)
    users = games[chatid]["p"]
    print(f"s:{games}")
    if query.data == 'join':
        query.answer("加入游戏")
        users[update.effective_user.first_name] = ""
        query.edit_message_text(getUsers(users),reply_markup=startkb)
        return
    elif query.data == 'start':
        timenow = datetime.now()
        if timenow > timer:
            query.answer("开始")
            query.edit_message_text(getUsers(users),reply_markup=gamekb)
            timer = datetime.now()+timedelta(seconds=5)
        else:
            query.answer("冷静！还没到五秒！",show_alert=True)
    elif query.data == 'big':
        if users == {}:
            return
        query.answer("你选择了大")
        users[update.effective_user.first_name] = "d"
        query.edit_message_text(getUsers(users),reply_markup=gamekb)
    elif query.data == 'small':
        if users == {}:
            return
        query.answer("你选择了小")
        users[update.effective_user.first_name] = "x"
        query.edit_message_text(getUsers(users),reply_markup=gamekb)
    elif query.data == 'sum':
        timenow = datetime.now()
        if timenow > timer:
            query.answer("结算开始")
            query.edit_message_text(sumGame(chatid))
            users = {}
        else:
            query.answer("冷静！还没到五秒！",show_alert=True)
    games[chatid]["p"] = users
    print(f"e:{games}")

def add_handler(dp:Dispatcher):
    guess_handler = CommandHandler('guess', guess)
    dp.add_handler(guess_handler)
    dp.add_handler(CallbackQueryHandler(buttonCallback))