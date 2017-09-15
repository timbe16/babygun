from app.util.db import db
import datetime


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail_from = db.Column(db.String(255))
    mail_to = db.Column(db.String(255))
    mail_cc = db.Column(db.String(255), nullable=False)
    mail_bcc = db.Column(db.String(255), nullable=False)
    mail_subj = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text)
    status = db.Column(db.Boolean)
    last_sent_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    counter = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "Email message #%s" % (self.id)


class EmailStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Text)
    sent_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    delivered = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return "Email status #%s" % (self.id)
