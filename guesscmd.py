from telegram.ext import Dispatcher,CommandHandler
import random

rnumber = random.randint(1,99)
ren = {}

def help():
    return "你需要猜一个数字，它是1-99里的。"

def guess(update, context):
    global rnumber
    if len(context.args) == 0:
        update.message.reply_text(help())
    else:
        print(context.args)
        if context.args[0].isdigit():
            number = int(context.args[0])
            fname = update.message.from_user.first_name
            if fname in ren:
                ren[fname] += 1
            else:
                ren[fname] = 1
            if number == rnumber:
                update.message.reply_text("你输入的是 %s 系统随机的是 %s 你猜中了！\n 新的随机数字生成了！"%(number,rnumber))
                rnumber = random.randint(1,99)
            elif number < rnumber:
                update.message.reply_text("你输入的是 %s 系统随机的是 %s 你猜小了！\n %s"%(number,rnumber,ren))
            elif number > rnumber:
                update.message.reply_text("你输入的是 %s 系统随机的是 %s 你猜大了！\n %s"%(number,rnumber,ren))
        else: 
            update.message.reply_text("你输入的%s不是数字"%context.args[0])

def add_handler(dp:Dispatcher):
    guess_handler = CommandHandler('guess', guess)
    dp.add_handler(guess_handler)

