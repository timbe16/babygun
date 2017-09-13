from app import app
from app.api.mail import mail_api

app.register_blueprint(mail_api)
