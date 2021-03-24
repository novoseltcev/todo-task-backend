from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from server.jwt_auth import owner_required
from server.errors.exc import InvalidSchema
from server.role import service as role_service
from server.role.service import RoleSchema

role_blueprint = Blueprint('role', __name__)
prefix = '/admin/role/'


@role_blueprint.route('/admin/roles/')
@owner_required()
def get():
    response = role_service.get_all()
    return jsonify(response)


@role_blueprint.route(prefix, methods=['POST'])
@owner_required()
def create():
    try:
        schema = RoleSchema(only=('name', 'description')).load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    id = role_service.create(**schema)
    schema['id'] = id
    return jsonify(schema), 202


@role_blueprint.route(prefix, methods=['PUT'])
@owner_required()
def update():
    try:
        schema = RoleSchema().load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    role = role_service.update(**schema)
    return jsonify(role), 202


@role_blueprint.route(prefix, methods=['DELETE'])
@owner_required()
def delete():
    try:
        id = RoleSchema(only=('id',)).load(request.json)['id']
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    role = role_service.delete(id)
    return jsonify(role), 202
