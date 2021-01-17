from telegram.ext import Dispatcher,CommandHandler,CallbackQueryHandler
from telegram import BotCommand,InputMediaAudio
import pafy
import os


def youtubemusic(update,context):
    if len(context.args) == 1:
        url = context.args[0]
        video = pafy.new(url)
        bestaudio = video.getbestaudio(preftype="m4a")
        filepath = f"/tmp/{bestaudio.title}.{bestaudio.extension}"
        music_size = bestaudio.get_filesize()
        if music_size > 1000*1000*10:
            update.message.reply_text("你要下载的音乐太大太长了，我们只下载小于10M的音乐！")
            return
        bestaudio.download(filepath=filepath)
        # msg = update.message.reply_text(f"正在下载音乐中，你的音乐有{music_size/1000}KB请稍后......")
        img = "https://pic1.zhimg.com/80/v2-47bb3dba233191ff5d1672dc4f624173_qhd.jpg"
        msg = update.message.reply_photo(img,caption=f"正在下载音乐中，你的音乐有{music_size/1000}KB请稍后......")
        msg = msg.edit_media(InputMediaAudio(open(filepath,'rb')))
        # msg.edit_caption("下载成功！")
        os.remove(filepath)
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