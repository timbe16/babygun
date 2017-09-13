import smtplib


class SMTP():
    def __init__(self, host, port, user, password):
        self.conn = None
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def open(self):
        if self.conn:
            return False

        self.conn = smtplib.SMTP(self.host, self.port)
        self.conn.ehlo()
        self.conn.starttls()
        self.conn.login(self.user, self.password)

        return self.conn

    def close(self):
        if self.conn:
            return self.conn.quit()
        return None

    def send_message(self, mail_from, mailto, message):
        if not mail_from or not mailto or not message:
            return False

        new_conn = self.open()

        response = {}#self.conn.sendmail(mail_from, mailto, message)

        if new_conn:
            self.close()

        return response
