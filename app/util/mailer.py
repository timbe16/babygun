from app import app
from app.util.smtp import SMTP

mailer = SMTP(host=app.config['SMTP_HOST'], port=app.config['SMTP_PORT'], user=app.config['SMTP_USER'], password=app.config['SMTP_PASSWD'])
