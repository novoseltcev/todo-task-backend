from flask import session, Blueprint, jsonify
from flask_apispec import use_kwargs

from . import service
from .schema import CategorySchema

from server import docs


category_blueprint = Blueprint('category', __name__)


@category_blueprint.route('/all', methods=['GET'])
def get():
    return jsonify(service.get_categories()), 200


@category_blueprint.route("/", methods=['POST'])
@use_kwargs(CategorySchema(only=('name',)))
def create(**kwargs):
    service.create_category(**kwargs)
    return service.get_category(**kwargs), 201


@category_blueprint.route("/", methods=['PUT'])
@use_kwargs(CategorySchema(only=('id', 'name')))
def edit(**kwargs):
    service.update_category(**kwargs)
    return service.get_category(**kwargs), 202


@category_blueprint.route("/", methods=['DELETE'])
@use_kwargs(CategorySchema(only=('id',)))
def delete(**kwargs):
    response = service.get_category(**kwargs)
    service.delete_category(**kwargs)
    return response, 202


docs.register(get, blueprint=category_blueprint.name)
docs.register(create, blueprint=category_blueprint.name)
docs.register(edit, blueprint=category_blueprint.name)
docs.register(delete, blueprint=category_blueprint.name)
