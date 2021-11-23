from copy import copy
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from marshmallow.fields import Email


class Message(object):
    def __init__(self):
        self.msg = MIMEMultipart('alternative')
        self.msg['From'] = 'no-reply@todotask.com'

    def set_body(self, html: str):
        self.msg.attach(MIMEText(html, 'html'))
        return self

    def set_target(self, target: Email):
        self.msg['To'] = target
        return self

    def set_subject(self, subject: str):
        self.msg['subject'] = subject
        return self

    def __copy__(self):
        tmp_msg = Message()
        tmp_msg.msg = copy(self.msg)

    def __str__(self):
        self.msg.as_string()
