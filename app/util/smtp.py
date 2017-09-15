import smtplib


class SMTP(object):
    def __init__(self, host, port, user, password):
        self.conn = None
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def open(self):
        if self.conn:
            return self.conn

        self.conn = smtplib.SMTP(self.host, self.port)
        self.conn.ehlo()
        self.conn.starttls()
        self.conn.login(self.user, self.password)

        return self.conn

    def close(self):
        if self.conn is not None:
            self.conn.quit()
            self.conn = None

        return None

    def send_message(self, mail_from, mailto, message):
        self.open()
        response = self.conn.sendmail(mail_from, mailto, message)
        self.close()

        return response
