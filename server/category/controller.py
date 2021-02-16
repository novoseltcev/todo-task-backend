from flask import request, session, Blueprint

from . import service


category_blueprint = Blueprint('category', __name__)


@category_blueprint.before_request
def check_json():
    json = request.json
    if not json:
        raise Exception("")


@category_blueprint.route('/')
def open_category():
    json = request.json
    res = service.open_category(json)
    session['current_category'] = json['id']
    session.modified = True
    return res


@category_blueprint.route("/", methods=['POST'])
def create_category():
    json = request.json
    res = service.create_category(json)
    category = service.category_rep.get_by_name(json['name'])  # TODO - нарушает абстракцию
    session['current_category'] = category.id
    session.modified = True
    return res


@category_blueprint.route("/", methods=['PUT'])
def edit_category():
    return service.update_category(request.json)


@category_blueprint.route("/", methods=['DELETE'])
def delete_category():
    json = request.json
    res = service.delete_category(json)
    if session.get('current_session', 1) == json['id']:  # TODO - сессия всегда должна быть известна
        session['current_category'] = 1
        session.modified = True
    return res
