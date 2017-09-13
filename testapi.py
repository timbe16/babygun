import unittest
import requests
import json
import re
from app import app


class TestMailApi(unittest.TestCase):
    def test_sendmail(self):
        response = requests.post('http://localhost:5000/api/mail/send',
                                 headers={'Client-Key': app.config["CLIENT_KEY"], 'Content-Type': 'application/json'},
                                 json={"to": app.config["SMTP_USER"],
                                       "from": app.config["SMTP_USER"],
                                       "subject": "test mail",
                                       "text": "test"})
        self.assertTrue(response.text.find('"status_code": 200'))


if __name__ == "__main__":
    unittest.main()
