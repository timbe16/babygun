import smtplib
import sys
from six import reraise as raise_


class SMTP(object):
    def __init__(self, host, port, user, password, timeout = 5):
        self.conn = None
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.timeout = timeout

    def send_message(self, mail_from, recipients, message):
        try:
            self.conn = smtplib.SMTP(host=self.host, port=self.port, timeout=self.timeout)
            self.conn.ehlo()
            self.conn.starttls()
            self.conn.login(self.user, self.password)
            response = self.conn.sendmail(mail_from, recipients, message)
        except Exception as e:
            traceback = sys.exc_info()[2]
            raise_(Exception, str(e), traceback)
        finally:
            if self.conn is not None:
                self.conn.quit()

        return response
