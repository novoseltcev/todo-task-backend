from flask import Blueprint, request, redirect
from marshmallow import ValidationError

from server import mail_redis_tokenlist, BaseConfig
from server.user import service as user_service
from server.email.schema import EmailSchema
from server.errors.exc import InvalidSchema, ForbiddenOperation
from server.jwt_auth import admin_required
from server.email import service as email_service


email_blueprint = Blueprint('email', __name__)


@email_blueprint.route('/admin/email/', methods=['POST'])
@admin_required(BaseConfig.admin_roles)
def send_notification():
    try:
        schema = EmailSchema(only=('emails', 'html', 'subject')).load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])
    email_service.send_message.delay(schema)


@email_blueprint.route('/user/confirm_email/<uuid:token>')
def confirm_email(token):
    token = str(token)
    id = mail_redis_tokenlist.get(token)
    if id is None:
        raise ForbiddenOperation()
    user_service.confirm_email(id)
    mail_redis_tokenlist.delete(token)
    return redirect('/')
