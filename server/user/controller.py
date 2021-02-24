from flask import Blueprint, request, jsonify, redirect, url_for

from server import login_manager
from . import service as user_service
from .schema import UserSchema


user_blueprint = Blueprint('user', __name__)
prefix = '/user/'


@user_blueprint.route(prefix, methods=['POST'])
def login():
    schema = UserSchema().load(request.json)
    if user_service.login(**schema):
        return redirect(url_for('index'))
    return jsonify(), 400


@user_blueprint.route(prefix, methods=['DELETE'])
def sign_out():
    schema = UserSchema().load(request.json)


@user_blueprint.route(prefix + 'register', methods=['POST'])
def register():
    schema = UserSchema().load(request.json)
