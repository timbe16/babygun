import atexit
import datetime
import json

from app import app
from sqlalchemy import func, exc
from app.model.email import Email, EmailStatus
from app.util.db import db
from app.util.mailer import mailer
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

JOB_INTERVAL_SEC = 60
SENDMAIL_INTERVAL_MIN = 10


def resend_mail():
    with app.app_context():
        mails_failed = Email.query \
            .filter(
            Email.status == False,
            Email.last_sent_at < (datetime.datetime.utcnow() - datetime.timedelta(minutes=SENDMAIL_INTERVAL_MIN)),
            Email.counter < 4
        ).all()

        for mail_message in mails_failed:
            app.logger.warning("Resending email #" + str(mail_message.id))
            mailto = [mail_message.mail_to]
            response = {}
            if mail_message.mail_cc is not None and mail_message.mail_cc:
                mailto += [mail_message.mail_cc]
            if mail_message.mail_bcc is not None and mail_message.mail_bcc:
                mailto += [mail_message.mail_bcc]

            try:
                response = mailer.send_message(mail_message.mail_from, mailto, mail_message.body)
            except Exception as e:
                app.logger.error(str(e))

            if len(response) > 0:
                app.logger.error('response')
                app.logger.error(response)

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
                db.session().rollback()
                app.logger.error('db error')
                app.logger.error(str(e))


with app.app_context():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=resend_mail, trigger=IntervalTrigger(seconds=JOB_INTERVAL_SEC))
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
