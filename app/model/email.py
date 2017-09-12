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

    def __repr__(self):
        return "Email message #%s" % (self.id)


class EmailStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Text)
    sent_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    delivered = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return "Email status #%s" % (self.id)
