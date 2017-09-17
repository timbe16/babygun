import requests
from app import app
from tests import TestCase


class TestEmail(TestCase):
    def test_sendmail(self):
        response = requests.post('http://localhost:5000/api/mail/send',
                                 headers={'Client-Key': app.config["CLIENT_KEY"], 'Content-Type': 'application/json'},
                                 json={"to": app.config["SMTP_USER"],
                                       "from": app.config["SMTP_USER"],
                                       "subject": "TestMailApiSendMessage",
                                       "text": "test"})
        r = response.json()
        mail_id = r.get("email_id", None)
        self.assertTrue(r["status_code"] >= 200 and r["status_code"] < 500)
        self.assertIsNotNone(mail_id)

    def test_sendmail_missing_recipients(self):
        response = requests.post('http://localhost:5000/api/mail/send',
                                 headers={'Client-Key': app.config["CLIENT_KEY"], 'Content-Type': 'application/json'},
                                 json={"from": app.config["SMTP_USER"],
                                       "subject": "TestMailApiSendMessage",
                                       "text": "test"})
        r = response.json()
        assert response.status_code == 400

    def test_sendmail_missing_from(self):
        response = requests.post('http://localhost:5000/api/mail/send',
                                 headers={'Client-Key': app.config["CLIENT_KEY"], 'Content-Type': 'application/json'},
                                 json={"from": app.config["SMTP_USER"],
                                       "subject": "TestMailApiSendMessage",
                                       "text": "test"})
        r = response.json()
        assert response.status_code == 400

    def test_sendmail_auth(self):
        response = requests.post('http://localhost:5000/api/mail/send',
                                 headers={'Client-Key': "thisiswrongkey", 'Content-Type': 'application/json'})
        assert response.status_code == 401
