from icalevents.icalevents import events
from datetime import date, timedelta,time
from telegram.ext import CommandHandler,CallbackContext,Dispatcher
from telegram import Update
import pytz

est = pytz.timezone('US/Eastern')

def timer_callback(context: CallbackContext):
    tomorrow = date.today() + timedelta(days=1)
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

def add_dispatcher(dp: Dispatcher):
    dp.add_handler(CommandHandler(["cal"], cal))


