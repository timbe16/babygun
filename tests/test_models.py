from app import app, db
from app.model.email import Email, EmailStatus
from tests import TestCase


class TestEmail(TestCase):
    def test_mail_creation(self):
        e = Email(mail_from='john@example.com',
                  mail_to="john@example.com",
                  mail_cc="john@example.com",
                  mail_bcc="john@example.com",
                  mail_subj="test subj",
                  body="test body",
                  status=False,
                  counter=0
                  )
        db.session.add(e)
        db.session.commit()

        assert Email.query.count() == 1


class TestEmailStatus(TestCase):
    def test_mail_status_creation(self):
        e = EmailStatus(email_id=1, status="", delivered=False)
        db.session.add(e)
        db.session.commit()

        assert EmailStatus.query.count() == 1
