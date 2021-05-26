from flask_mail import Message
from server import celery, mail


@celery.task(name='email.confirm')
def send_message(subject: str, emails: list, html):
    msg = Message(subject,
                  recipients=emails,
                  )
    msg.html = html
    mail.send(msg)
