from app import app
from flask import Blueprint, request, jsonify
from app.api.api_helper import required_param, optional_param
from app.util.authentication import auth_token_required, ERROR_LEVEL_API
from app.model.email import Email, EmailStatus
from app.util.db import db
from app.util.mailer import mailer
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from sqlalchemy import desc, exc
import bleach
import json

mail_api = Blueprint("mail_api", __name__, url_prefix='/api/mail')


@mail_api.route('/send', methods=['POST'])
@auth_token_required
def sendmail():
    """Send email to specific addresses.

    .. :quickref: Send email

    :param json (to, from, cc, bcc, subject, text):
    :returns: int status_code, int email_id, str error_message
    | Status code list:
    | 200 - ok, message sent
    | 300 - message sending is in progress
    | 400 - wrong input params
    | 401 - invalid client key
    | 500 - internal error, something goes wrong
    :rtype: json
    """

    response_dictionary = {'status_code': 300}
    response = {}
    content = request.get_json(force=True)
    mail_from = required_param(content, "from", str)
    mail_to = required_param(content, "to", str)
    mail_cc = optional_param(content, "cc", str)
    mail_bcc = optional_param(content, "bcc", str)
    mail_subj = bleach.clean(optional_param(content, "subject", str))
    mail_body = bleach.clean(optional_param(content, "text", str))
    recipients = [mail_to]
    if mail_cc is not None:
        recipients += [mail_cc]
    else:
        mail_cc = ""
    if mail_bcc is not None:
        recipients += [mail_bcc]
    else:
        mail_bcc = ""

    # Prepare message
    message = MIMEMultipart()
    message["Subject"] = Header(mail_subj, 'utf-8')
    message["From"] = mail_from
    message["To"] = mail_to
    message["Cc"] = mail_cc
    message["Bcc"] = mail_bcc
    message.attach(MIMEText(mail_body.encode('utf-8'), 'plain', 'utf-8'))

    try:
        mail = Email(mail_from=mail_from,
                     mail_to=mail_to,
                     mail_cc=mail_cc,
                     mail_bcc=mail_bcc,
                     mail_subj=mail_subj,
                     body=message.as_string(),
                     status=False,
                     counter=0
                     )
        db.session.add(mail)
        db.session.commit()
        response_dictionary['email_id'] = mail.id
    except (Exception, exc) as e:
        db.session.rollback()
        response_dictionary['status_code'] = 500
        response_dictionary['error_message'] = "db error"
        app.logger.error(str(e))
        return jsonify(**response_dictionary)

    return jsonify(**response_dictionary)


@mail_api.route('/get_status/<int:id>', methods=['GET'])
@auth_token_required
def get_status(id):
    """Get email delivery status.

    .. :quickref: Get email delivery status

    :param int (email_id):
    :returns: bool status
    :rtype: json
    """
    response_dictionary = {}
    try:
        mail = Email.query.filter(Email.id == id).first()
        response_dictionary['status'] = mail.status
    except (Exception, exc) as e:
        response_dictionary['status_code'] = 500
        response_dictionary['error_message'] = "db error"
        app.logger.error(str(e))

    return jsonify(**response_dictionary)
