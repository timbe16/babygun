import atexit
import datetime
import json
from app import app
from sqlalchemy import exc
from app.model.email import Email, EmailStatus
from app.util.db import db
from app.util.mailer import mailer
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

JOB_INTERVAL_SEC = 10
RETRY_INTERVAL_MIN = 10


def send_mail():
    with app.app_context():
        mails_new = Email.query \
            .filter(
            Email.status == False,
            Email.counter == 0
        ).all()
        mails_failed = Email.query \
            .filter(
            Email.status == False,
            Email.last_sent_at < (datetime.datetime.utcnow() - datetime.timedelta(minutes=RETRY_INTERVAL_MIN)),
            Email.counter < 4
        ).all()

        for mail_message in mails_new + mails_failed:
            app.logger.info("Sending email #" + str(mail_message.id))
            recipients = [mail_message.mail_to]
            response = {}
            if mail_message.mail_cc is not None and mail_message.mail_cc:
                recipients += [mail_message.mail_cc]
            if mail_message.mail_bcc is not None and mail_message.mail_bcc:
                recipients += [mail_message.mail_bcc]

            try:
                response = mailer.send_message(mail_message.mail_from, recipients, mail_message.body)
            except Exception as e:
                app.logger.error(str(e))
                response["error"] = "smtp exception"

            if len(response) > 0:
                app.logger.error('response: ' + str(response))

            try:
                mail_message.last_sent_at = datetime.datetime.utcnow()
                mail_message.counter = mail_message.counter + 1
                mail_message.status = False if len(response) > 0 else True
                mail_status = EmailStatus(email_id=mail_message.id,
                                          status=json.dumps(response),
                                          delivered=False if len(response) > 0 else True
                                          )
                db.session.add(mail_status)
                db.session.commit()
            except (Exception, exc) as e:
                db.session.rollback()
                app.logger.error('db error: ' + str(e))


with app.app_context():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=send_mail, trigger=IntervalTrigger(seconds=JOB_INTERVAL_SEC))
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
