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

SEND_INTERVAL_SEC = 60


def resend_mail():
    with app.app_context():
        since = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
        to = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)
        mails_failed = EmailStatus.query \
            .filter(EmailStatus.delivered == False, EmailStatus.sent_at > since, EmailStatus.sent_at < to) \
            .having(func.count_(EmailStatus.delivered) <= 2) \
            .group_by(EmailStatus.email_id, EmailStatus.delivered).all()
        result = EmailStatus.query.filter(EmailStatus.delivered == True, EmailStatus.sent_at > since).all()
        mails_success = [r.email_id for r in result]

        for m in mails_failed:
            if m.email_id in mails_success:
                continue
            app.logger.warning("Resending email #" + str(m.email_id))
            mail_message = Email.query.filter(Email.id == m.email_id).first()
            mailto = [mail_message.mail_to]
            if mail_message.mail_cc is not None:
                mailto += [mail_message.mail_cc]
            else:
                mail_message.mail_cc = ""
            if mail_message.mail_bcc is not None:
                mailto += [mail_message.mail_bcc]
            else:
                mail_message.mail_bcc = ""
            try:
                response = mailer.send_message(mail_message.mail_from, mailto, mail_message.body)
            except Exception as e:
                app.logger.error(str(e))

            if len(response) > 0:
                app.logger.error('response')
                app.logger.error(response)

            try:
                mail_status = EmailStatus(email_id=m.email_id,
                                          status=json.dumps(response),
                                          delivered=False if len(response) > 0 else True
                                          )
                db.session.add(mail_status)
                db.session.commit()
            except (Exception, exc) as e:
                db.session().rollback()
                app.logger.error('db error')
                app.logger.error(str(e))


scheduler = BackgroundScheduler()
scheduler.add_job(func=resend_mail, trigger=IntervalTrigger(seconds=SEND_INTERVAL_SEC))
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
