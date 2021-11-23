from flask import Blueprint, request, redirect, Response
from marshmallow import ValidationError

from server import mail_redis_tokenlist, BaseConfig
from server.services.mail.schema import MailSchema
from server.errors.exc import InvalidSchema, ForbiddenOperation
from server.jwt_auth import admin_required
from server.services.mail import service as email_service

mail_blueprint = Blueprint('mail', __name__)


@mail_blueprint.route('/admin/mail/', methods=['POST'])
@admin_required(BaseConfig.admin_roles)
def send_notification():
    try:
        schema = MailSchema(only=('emails', 'html', 'subject')).load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])
    email_service.send_message.delay(schema)

