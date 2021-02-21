from flask import session, Blueprint, jsonify
from flask_apispec import use_kwargs

from . import service
from .schema import CategorySchema
from server import docs


category_blueprint = Blueprint('category', __name__)


@category_blueprint.route('/open', methods=['POST'])
@use_kwargs(CategorySchema(only=('id',)))
def open_category(**kwargs):
    service.open_category(**kwargs)
    session['current_category'] = kwargs['id']
    session.modified = True
    res = service.get_category(**kwargs)
    return {'category': res, 'current_category': session['current_category']}, 200


@category_blueprint.route('/all', methods=['GET'])
def get():
    return jsonify(service.get_categories()), 200


@category_blueprint.route("/", methods=['POST'])
@use_kwargs(CategorySchema(only=('name',)))
def create(**kwargs):
    service.create_category(**kwargs)
    new_category = service.get_category(**kwargs)
    session['current_category'] = new_category['id']
    session.modified = True
    return new_category, 201


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
    if session['current_category'] == kwargs['id']:
        session['current_category'] = 1
        session.modified = True
    return response, 202


docs.register(open_category, blueprint=category_blueprint.name)
docs.register(create, blueprint=category_blueprint.name)
docs.register(edit, blueprint=category_blueprint.name)
docs.register(delete, blueprint=category_blueprint.name)
