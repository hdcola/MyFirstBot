from icalevents.icalevents import events
from datetime import date, timedelta,time
from telegram.ext import CommandHandler,CallbackContext,Dispatcher
from telegram import Update
import pytz
import config

est = pytz.timezone('US/Eastern')
cs = config.CONFIG['cs']

def timer_callback(context: CallbackContext):
    tomorrow = date.today() + timedelta(days=1)
    # chatid = context.job_queue.context
    url = "webcal://p60-caldav.icloud.com/published/2/MTMwMjQzNDk4NDEzMDI0M3sQtDCMMqfWL7VMca-urO1PHNC7k1S3xOJlT4pbFvB2zTOKsoMYKAaoX8kwofUBGi0yjak_7FqpXGZUZh5MhGY"
    es = events(url,fix_apple=True,start=tomorrow,end=tomorrow)
    msg = ""
    for e in es:
        msg += f"{e.summary} start:{e.start} end:{e.end} {e.description}"
    msg += f"下次发送时间{context.job.next_t.astimezone(est)}"
    context.bot.send_message(chat_id=context.job.context,text=msg)

def cal(update: Update,context:CallbackContext ):
    chat_id = update.effective_chat.id
    j = context.job_queue.run_repeating(timer_callback,5,context=chat_id)
    update.effective_message.reply_text(f"开始定时发送，下次发送时间:{j.next_t}")

def run_repeating(job_queue):
    chat_id = -1001366387264
    job_queue.run_daily(timer_callback,time(hour=11,minute=50,tzinfo=pytz.timezone('US/Eastern')),context=chat_id)

def calhelp(update,context):
    chatid = str(update.effective_chat.id)
    group = str(update.effective_chat.type)
    if group == 'supergroup' or group == 'group' or group == 'channel':
        groupname = update.effective_chat.title
    elif group == 'private':
        groupname = update.effective_chat.first_name
    if not chatid in cs:
        cs[chatid] = {}
        cs[chatid]['url'] = ''
        cs[chatid]['hours'] = 0
        cs[chatid]['minutes'] = 0
        cs[chatid]['tz'] = ''
        cs[chatid]['title'] = ''
    # setcal [Your Apple Calendar URL Here] [The Time You Want The Notification Sent, For Example, 17:00] [Your Time Zone]
    if len(context.args) == 3:
        url = str(context.args[0])
        time = context.args[1]
        timezone = context.args[2]
        if timezone in pytz.all_timezones:
            cs[chatid]['tz'] = timezone
            update.message.reply_text(f"Success! You will receive a notification from Dank Premium in THIS CHAT everyday at {time}.")
        else:
            update.message.reply_text(f'Invaid timezone.\n\nHere is a link of a list of all the timezones:\n\n✨https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568#file-pytz-time-zones-py')
            
        cs[chatid]['url'] = url
        cs[chatid]['hours'] = int(time.split(':')[0])
        cs[chatid]['title'] = groupname
        if int(time.split(':')[1]) < 10:
            minutes = time.split(':')[1][1:]
            cs[chatid]['minutes'] = int(minutes)
        else:
            cs[chatid]['minutes'] = int(time.split(':')[1])
        config.save_config()
        # context.job_queue.run_daily(timer_callback,
        #     time(hour=cs[chatid]['hours'],minute=cs[chatid]['minutes'],tzinfo=pytz.timezone(cs[chatid]['tz'])),
        #     context=chatid)
        run_repeating(context.job_queue)
        jobs = context.job_queue.jobs()
        for j in jobs:
            print(f"{j.name} {j.next_t}\n\n")
    else:
        update.message.reply_text('䷦ Structure: \n\n/setcal@dankpbot [Your Apple Calendar URL Here] [The Time You Want The Notification Sent, For Example, 17:00] [Your Time Zone]')

def view_cal(update,context):
    minutes = ''
    msg = ''
    for chatid in list(cs):
        if cs[chatid]['minutes'] < 10:
            minutes = f"0{cs[chatid]['minutes']}"
        else:
            minutes = cs[chatid]['minutes']
        msg += f"✨ {cs[chatid]['title']}\n📆 Calendar URL: {cs[chatid]['url']}\n🔔 Notification Time: {cs[chatid]['hours']}:{minutes}\n\n"
    update.message.reply_text(msg)

def add_dispatcher(dp: Dispatcher):
    dp.add_handler(CommandHandler(["cal"], cal))
    dp.add_handler(CommandHandler('setcal', calhelp))
    dp.add_handler(CommandHandler('showcal', view_cal))