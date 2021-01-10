from telegram.ext import Dispatcher,CommandHandler,CallbackQueryHandler
from telegram import BotCommand
import pafy

def youtubemusic(update,context):
    if len(context.args) == 1:
        url = context.args[0]
        video = pafy.new(url)
        update.message.reply_text(str(video) )
    else:
        update.message.reply_text("请告诉我URL啊，不然我去给你变啊？！")

def add_handler(dp:Dispatcher):
    dp.add_handler(CommandHandler('ytm', youtubemusic))

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=iqL1BLzn3qc"
    video = pafy.new(url)
    bestaudio = video.getbestaudio(preftype="m4a")
    print(bestaudio)
    filepath = f"/tmp/{bestaudio.title}.{bestaudio.extension}"
    bestaudio.download(filepath=filepath)
    print(bestaudio.url)