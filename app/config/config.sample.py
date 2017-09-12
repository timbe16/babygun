import os

INSTANCE_TYPE = os.getenv("INSTANCE_TYPE", "LOCAL")

SQLALCHEMY_TRACK_MODIFICATIONS = False
if INSTANCE_TYPE == "LOCAL":
    # sqlite for demo only
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:////' + os.path.dirname(os.path.abspath(__file__)) + '/app.db')
else:
    pass

SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = os.getenv('SMTP_PORT', 587)
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASSWD = os.getenv('SMTP_PASSWD', '')

CLIENT_KEY = os.getenv("CLIENT_KEY", "kSOVNpXFAXng6GSDAjope1EUHe0QtV")
SECRET_KEY = os.getenv("SECRET_KEY", "k9WBC9APGPhNkbPe0z3hEHDtWV5zNQ")