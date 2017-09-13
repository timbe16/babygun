from flask import Blueprint, request, jsonify
from .api_helper import *
from app.util.authentication import auth_token_required, ERROR_LEVEL_API
from app.model.email import Email, EmailStatus
from app.util.db import db
from app.util.smtp import SMTP
from sqlalchemy import desc
import smtplib
import bleach
import json
import sys

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

    response_dictionary = {'status_code': 200}
    content = request.get_json(force=True)
    mail_from = required_param(content, "from", str)
    mail_to = required_param(content, "to", str)
    mail_cc = optional_param(content, "cc", str)
    mail_bcc = optional_param(content, "bcc", str)
    mail_subj = bleach.clean(optional_param(content, "subject", str))
    mail_body = bleach.clean(optional_param(content, "text", str))
    mailto = [mail_to]
    if mail_cc is not None:
        mailto += [mail_cc]
    else:
        mail_cc = ""
    if mail_bcc is not None:
        mailto += [mail_bcc]
    else:
        mail_bcc = ""

    # Prepare message
    message = """From: %s\nTo: %s\nCc: %s\nBcc: %s\nSubject: %s\n\n%s""" % (mail_from, mail_to, mail_cc, mail_bcc, mail_subj, mail_body)
    try:
        mailer = SMTP(host=app.config['SMTP_HOST'], port=app.config['SMTP_PORT'], user=app.config['SMTP_USER'], password=app.config['SMTP_PASSWD'])
        response = mailer.send_message(mail_from, mailto, message)
        print "response:"
        print response
        # response = {"err": 1}
        if response is False:
            response_dictionary['status_code'] = 500
    except:
        response_dictionary['status_code'] = 500

    mail = Email(mail_from=mail_from,
                 mail_to=mail_to,
                 mail_subj=mail_subj,
                 body=mail_body
                 )
    db.session.add(mail)
    db.session.commit()
    response_dictionary['email_id'] = mail.id
    mail_status = EmailStatus(email_id=mail.id,
                              status=json.dumps(response),
                              delivered=False if response_dictionary['status_code'] != 200 else True
                              )
    db.session.add(mail_status)
    db.session.commit()

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
    mail = EmailStatus.query.filter(EmailStatus.email_id == id).order_by(desc(EmailStatus.sent_at)).first()
    response_dictionary['status'] = mail.delivered

    return jsonify(**response_dictionary)
