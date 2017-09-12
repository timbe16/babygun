from app import app
# from app.api.user_api import user_api
# from app.api.reset_password_api import reset_password_api
# from app.api.push import push_api
# from app.api.paytollo import paytollo_api
from app.api.mail import mail_api

# app.register_blueprint(user_api)
# app.register_blueprint(reset_password_api)
# app.register_blueprint(push_api)
# app.register_blueprint(paytollo_api)
app.register_blueprint(mail_api)