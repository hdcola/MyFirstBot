from telegram.ext import Updater,MessageHandler, Filters,CommandHandler
from telegram import BotCommand
import os

def read_file_as_str(file_path):
    # 判断路径文件存在
    if not os.path.isfile(file_path):
        raise TypeError(file_path + " does not exist")

    # 读取文件内容到all_the_text
    all_the_text = open(file_path).read()
    # print type(all_the_text)
    return all_the_text

TOKEN=read_file_as_str('TOKEN')
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

import game24

commands = game24.add_handler(dispatcher)
updater.bot.set_my_commands(commands)

updater.start_polling()
updater.idle()