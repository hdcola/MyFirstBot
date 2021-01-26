from telegram.ext import Dispatcher,CommandHandler,CallbackQueryHandler,InlineQueryHandler,CallbackContext
from telegram import BotCommand,InlineQueryResultGame,Update
from uuid import uuid4

def inlinequery(update: Update, context: CallbackContext):
    results = [
        InlineQueryResultGame(id=str(uuid4()),game_short_name="test")
    ]
    update.inline_query.answer(results)

def game(update: Update, context: CallbackContext):
    update.effective_chat.send_game(game_short_name="test")

def game_callbak(update: Update, context: CallbackContext):
    query = update.callback_query
    # query.answer(url=f"https://hdcola.github.io/p5js/gametest/index.html?id={query.id}")
    query.answer(url=f"http://127.0.0.1:5500/gametest/index.html?id={query.id}")


def add_handler(dp:Dispatcher):
    dp.add_handler(InlineQueryHandler(inlinequery))
    dp.add_handler(CommandHandler("game",game))
    dp.add_handler(CallbackQueryHandler(game_callbak))