import unittest
import requests
from app import app


class TestMailApiSendMessage(unittest.TestCase):
    def test_sendmail(self):
        response = requests.post('http://localhost:5000/api/mail/send',
                                 headers={'Client-Key': app.config["CLIENT_KEY"], 'Content-Type': 'application/json'},
                                 json={"to": app.config["SMTP_USER"],
                                       "from": app.config["SMTP_USER"],
                                       "subject": "TestMailApiSendMessage",
                                       "text": "test"})
        r = response.json()
        self.assertTrue(r["status_code"] == 200)


if __name__ == "__main__":
    unittest.main()
