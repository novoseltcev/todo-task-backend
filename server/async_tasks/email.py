from uuid import uuid4

from flask import render_template
from flask_mail import Message
from server import celery, mail, Config, mail_redis_tokenlist


@celery.task(name='email.confirm')
def confirm_registration(user):
    confirm_uuid = uuid4()
    endpoints = {
        'confirm': '/user/confirm_email/token=' + str(confirm_uuid),
        'contact': "/contact",
        'privacy': "/privacy",
        'terms': "/terms"
    }
    urls = {key: Config.DOMAIN + value for key, value in endpoints.items()}
    msg_html = render_template('email_confirm.html', recipient=user.email, urls=urls)
    msg = Message(msg_html,
                  recipients=(user.email, )
                  )
    mail_redis_tokenlist.set(confirm_uuid, user.id, ex=Config.MAIL_CONFIRM_TOKEN_EXPIRES)
    mail.send(msg)

