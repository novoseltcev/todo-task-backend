from copy import copy
from uuid import uuid4
from typing import NoReturn

from ._repositoryABC import Mails
from ._serviceABC import MailService
from .model import Message
from .schema import MailSchema


class MailLogic(MailService):
    @staticmethod
    def notify(schema: MailSchema) -> NoReturn:
        emails = schema.consumers

        msg_prototype = Message()\
            .set_subject(schema.subject)\
            .set_body(schema.html)

        messages = (copy(msg_prototype).set_body(email) for email in emails)
        for message in messages:
            Mails.send(message)

    @staticmethod
    def confirm(schema: MailSchema) -> NoReturn:
        confirm_uuid = uuid4()
        email = schema.consumers[0]
        Mails.link(email, confirm_uuid)
        message = Mails.get_confirm_mail(email, confirm_uuid)
        Mails.send(message)

    # mail_redis_tokenlist.set(str(confirm_uuid), id, ex=BaseConfig.MAIL_CONFIRM_TOKEN_EXPIRES)
    # html = render_template('email_confirm.html', recipient=email, urls=urls)