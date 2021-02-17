from flask import session, Blueprint
from flask_apispec import use_kwargs

from . import service
from .schema import CategorySchema
from server.local import response
from server import docs


category_blueprint = Blueprint('category', __name__)


@category_blueprint.route('/')
@use_kwargs(CategorySchema(only=('id',)))
def open_category(**kwargs):
    service.open_category(**kwargs)
    session['current_category'] = kwargs['id']
    session.modified = True
    return response(**service.get_categories(), code=200)


@category_blueprint.route("/", methods=['POST'])
@use_kwargs(CategorySchema(only=('name',)))
def create(**kwargs):
    service.create_category(**kwargs)
    new_category = service.get_category(**kwargs)
    session['current_category'] = new_category['id']
    session.modified = True
    return response(**service.get_categories(), code=201)


@category_blueprint.route("/", methods=['PUT'])
@use_kwargs(CategorySchema(only=('id', 'name')))
def edit(**kwargs):
    service.update_category(**kwargs)

    return response(**service.get_categories(), code=202)


@category_blueprint.route("/", methods=['DELETE'])
@use_kwargs(CategorySchema(only=('id',)))
def delete(**kwargs):
    service.delete_category(**kwargs)
    if session['current_category'] == kwargs['id']:
        session['current_category'] = 1
        session.modified = True
    return response(**service.get_categories(), code=202)


docs.register(open_category, blueprint=category_blueprint.name)
docs.register(create, blueprint=category_blueprint.name)
docs.register(edit, blueprint=category_blueprint.name)
docs.register(delete, blueprint=category_blueprint.name)
