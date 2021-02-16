from flask import request, session, Blueprint
from flask_apispec import use_kwargs

from . import service
from .schema import CategorySchema


category_blueprint = Blueprint('category', __name__)


@category_blueprint.before_request
def check_json():
    json = request.json
    if not json:
        raise Exception("")


@category_blueprint.route('/')
@use_kwargs(CategorySchema(only=('id',)))
def open_category(**kwargs):
    res = service.open_category(**kwargs)
    session['current_category'] = kwargs['id']
    session.modified = True
    return res


@category_blueprint.route("/", methods=['POST'])
@use_kwargs(CategorySchema(only=('name',)))
def create_category(**kwargs):
    res = service.create_category(**kwargs)
    new_category = service.category_rep.get_by_name(kwargs['name'])  # TODO - нарушает абстракцию
    session['current_category'] = new_category.id
    session.modified = True
    return res


@category_blueprint.route("/", methods=['PUT'])
@use_kwargs(CategorySchema(only=('id', 'name')))
def edit_category(**kwargs):
    return service.update_category(**kwargs)


@category_blueprint.route("/", methods=['DELETE'])
@use_kwargs(CategorySchema(only=('id',)))
def delete_category(**kwargs):
    res = service.delete_category(**kwargs)
    if session['current_category'] == kwargs['id']:
        session['current_category'] = 1
        session.modified = True
    return res
