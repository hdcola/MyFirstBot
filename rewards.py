
from telegram.ext import Dispatcher,CommandHandler


def rewards(update, context):
    update.message.reply_text("来啦来啦")

def add_handler(dp:Dispatcher):
    start_handler = CommandHandler('rewards', rewards)
    dp.add_handler(start_handler)
