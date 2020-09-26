from telegram.ext import Dispatcher,CommandHandler


def guess(update, context):
    update.message.reply_text("来啦来啦")

def add_handler(dp:Dispatcher):
    guess_handler = CommandHandler('guess', guess)
    dp.add_handler(guess_handler)