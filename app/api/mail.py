from flask import Blueprint, request, jsonify
from .api_helper import *
from app.util.authentication import auth_token_required, ERROR_LEVEL_API
from app.model.email import Email, EmailStatus
from app.util.db import db
import smtplib
import bleach
import json

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
    mail_subj = bleach.clean(optional_param(content, "subject", str))
    mail_body = bleach.clean(optional_param(content, "text", str))
    mailto = [mail_to]
    if not mail_cc:
        mailto += [mail_cc]
    if not mail_bcc:
        mailto += [mail_bcc]

    # Prepare message
    message = """From: %s\nTo: %s\nCc: %s\nBcc: %s\nSubject: %s\n\n%s""" % (mail_from, mail_to, mail_cc, mail_bcc, mail_subj, mail_body)
    try:
        server = smtplib.SMTP(app.config['SMTP_HOST'], app.config['SMTP_PORT'])
        server.ehlo()
        server.starttls()
        server.login(app.config['SMTP_USER'], app.config['SMTP_PASSWD'])
        response = server.sendmail(mail_from, mailto, message)
        print "response"
        print response
        print type(response)
        server.close()
        response_dictionary['status_code'] = 200
    except:
        response_dictionary['status_code'] = 500

    if len(response) > 0:
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
