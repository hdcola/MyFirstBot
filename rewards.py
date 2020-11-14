
from telegram.ext import Dispatcher,CommandHandler
from telegram import BotCommand


def rewards(update, context):
    update.message.reply_text("来啦来啦")

def add_handler(dp:Dispatcher):
    start_handler = CommandHandler('rewards', rewards)
    dp.add_handler(start_handler)

def get_command():
    return [BotCommand('rewards','其实这里什么都没写')]