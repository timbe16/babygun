from flask import Blueprint, request, jsonify
from .api_helper import *
from app.util.authentication import auth_token_required, ERROR_LEVEL_API
from app.model.email import Email, EmailStatus
import smtplib

mail_api = Blueprint("mail_api", __name__, url_prefix='/api/mail')


@mail_api.route('/send', methods=['POST'])
@auth_token_required
def sendmail():
    """Send email to specific addresses.

    .. :quickref: Send email

    :param json (to, from, cc, bcc, subject, text):
    :returns: int status_code, int email_id
    :rtype: json
    """

    response_dictionary = {}
    content = request.get_json(force=True)
    mail_from = required_param(content, "from", str)
    mail_to = required_param(content, "to", str)
    mail_cc = optional_param(content, "cc", str)
    mail_bcc = optional_param(content, "bcc", str)
    mail_subj = optional_param(content, "subject", str)
    mail_body = optional_param(content, "text", str)

    # Prepare actual message
    # message = """From: %s\nTo: %s\nCc: %s\nBcc: %s\nSubject: %s\n\n%s""" % (mail_from, mail_to, mail_cc, mail_bcc, mail_subj, mail_body)
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (mail_from, mail_to, mail_subj, mail_body)
    try:
        server = smtplib.SMTP(app.config['SMTP_HOST'], app.config['SMTP_PORT'])
        server.ehlo()
        server.starttls()
        server.login(app.config['SMTP_USER'], app.config['SMTP_PASSWD'])
        response = server.sendmail(mail_from, mail_to, message)
        server.close()
        response_dictionary['status_code'] = 200
    except:
        response_dictionary['status_code'] = 500

    # push = Push.query.filter(Push.user_id == user.id, Push.push_type == 'default', Push.apn_token == apn_token).first()
    # if not push:
    #     push = Push()
    #     push.apn_token = apn_token
    #     push.device_udid = device_udid
    #     push.push_type = 'default'
    #     user.pushes.append(push)
    #     db.session.commit()


    return jsonify(**response_dictionary)


@mail_api.route('/get_status', methods=['POST'])
@auth_token_required
def get_status():
    """Get email delivery status.

    .. :quickref: Get email delivery status

    :param json (email_id):
    :returns: int status_code
    :rtype: json
    """
    pass
