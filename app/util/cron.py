import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger


def resend_mail():
    print time.strftime("%A, %d. %B %Y %I:%M:%S %p")


scheduler = BackgroundScheduler()
scheduler.add_job(func=resend_mail, trigger=IntervalTrigger(seconds=160))
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
