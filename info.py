from telegram import Update,Animation, PhotoSize
from telegram.ext import Dispatcher,CommandHandler,CallbackContext
from json import dumps,loads

msg_type = {
    "video":["file_id","file_unique_id","width","height","duration"],
    "photo":["file_id","file_unique_id","width","height","file_size"],
    "audio":["file_id","file_unique_id","duration","performer","title","mime_type","file_size"],
    "animation":["file_id","file_unique_id","width","height","duration"],
    "sticker":["file_id","file_unique_id","width","height","is_animated"],
    "videomsg":["file_id","file_unique_id","length","duration"],
    "voicemsg":["file_id","file_unique_id","duration","mime_type","file_size"]
}

def listtojson(objs):
    r = ""
    count = 0
    for obj in objs:
        count += 1
        r += f"\n第{count}个"
        r += tojson(obj)
    return r

def tojson(obj):
    return dumps(eval(str(obj)),indent=2)

def getobjinfo (msgtype,msgobj):
    rmsg = ""
    for i in msg_type[msgtype]:
        # rmsg += str(f'{i} = {msgobj.__dict__[i]},\n\n')
        rmsg += str(f'{i} = {getattr(msgobj,i)},\n\n')
    return rmsg

def info(update:Update,context: CallbackContext):
    if update.effective_message.reply_to_message:
        msg = update.effective_message.reply_to_message
        rmsg = ""
        if msg.audio:
            audio = update.message.reply_to_message.audio
            rmsg = getobjinfo('audio',audio)
            update.message.reply_audio(audio,caption=rmsg)
        if msg.animation:
            animation = update.message.reply_to_message.animation
            rmsg = getobjinfo('animation',animation)
            update.message.reply_animation(animation,caption=rmsg)
    else:
        update.message.reply_text(text=tojson(update.effective_message))

def add_dispatcher(dp: Dispatcher):
    dp.add_handler(CommandHandler(["info"], info))
