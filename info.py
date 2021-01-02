from telegram import Update,Animation, PhotoSize
from telegram.ext import Dispatcher,CommandHandler,CallbackContext
from json import dumps,loads

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

def info(update:Update,context: CallbackContext):
    if update.effective_message.reply_to_message:
        msg = update.effective_message.reply_to_message
        msg_attr = {}
        if msg.audio:
            msg_attr["Audio"] = tojson(msg.audio)
        if msg.animation:
            msg_attr["Animation"] = tojson(msg.animation)
        if msg.photo:
            msg_attr["Photo"] = listtojson(msg.photo)
        if msg.video:
            msg_attr["Video"] = tojson(msg.video)
        if len(msg_attr)==0:
            msg_attr["不知道是什么东东"] = tojson(msg)
        r = ""
        for a in msg_attr:
            r = f"类型：{a}\n{msg_attr[a]}\n"
        update.message.reply_text(text=r)
    else:
        update.message.reply_text(text=tojson(update.effective_message))

def hdinfo(update:Update,context: CallbackContext):
    update.message.reply_text(text=tojson(update.effective_message))

def add_dispatcher(dp: Dispatcher):
    dp.add_handler(CommandHandler(["info"], info))
    dp.add_handler(CommandHandler(["hdinfo"], hdinfo))