from uuid import uuid4

from flask import render_template

from server import BaseConfig, mail_redis_tokenlist
from server.async_tasks.email import send_message


def html_confirm_registration(id, email):
    confirm_uuid = uuid4()
    endpoints = {
        'confirm': '/user/confirm_email/' + str(confirm_uuid),
        'contact': "/contact",
        'privacy': "/privacy",
        'terms': "/terms"
    }
    urls = {key: BaseConfig.CORS_ALLOWED_ORIGINS[0] + value for key, value in endpoints.items()}
    mail_redis_tokenlist.set(str(confirm_uuid), id, ex=BaseConfig.MAIL_CONFIRM_TOKEN_EXPIRES)
    html = render_template('email_confirm.html', recipient=email, urls=urls)
    return html
