from telegram.ext import Dispatcher,CommandHandler,MessageHandler,Filters,CallbackContext
from telegram import BotCommand,Update
import random

# {chatid:
#       'cards':[]
# }
games = {}

def set_games_cards(chatid,cards):
    games[chatid] = {}
    games[chatid]['cards'] = cards

def start(update:Update,context:CallbackContext):
    chatid = update.effective_chat.id
    cards = random.sample([1,2,3,4,5,6,7,8,9,10],4)
    update.effective_message.reply_text(f"{cards[0]},{cards[1]},{cards[2]},{cards[3]}")
    set_games_cards(chatid,cards)

def question(update,context):
    chatid = update.effective_chat.id
    update.effective_message.reply_text(f"当卡牌为：{games[chatid]['cards']}")

def end(update,context):
    pass

def answer(update,context):
    pass

def add_handler(dp:Dispatcher):
    dp.add_handler(CommandHandler('start24', start))
    dp.add_handler(CommandHandler('q', question))
    dp.add_handler(CommandHandler('end24', end))
    dp.add_handler(MessageHandler(Filters.chat_type.supergroup & Filters.text , answer))
    return [BotCommand('start24','开始一个24点游戏'),BotCommand('q','查询当前进行中的24点游戏'),BotCommand('end24','结束当前进行的游戏')]