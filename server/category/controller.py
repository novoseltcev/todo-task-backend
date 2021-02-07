from flask import request, session
from server.category import service
from flask import Blueprint


category_blueprint = Blueprint('category', __name__)


@category_blueprint.route('/')
def open_category():
    json = request.json
    id = json['id']
    res = service.open_category(id)
    session['current_category'] = id
    session.modified = True
    return res


@category_blueprint.route("/", methods=['POST'])
def create_category():
    json = request.json
    name = json["name"]
    res = service.create_category(name)
    category = service.category_rep.get_by_name(name)  # TODO - нарушает абстракцию
    session['current_category'] = category[0]
    session.modified = True
    return res


@category_blueprint.route("/", methods=['PUT'])
def edit_category():
    json = request.json
    id = json['id']
    source = json['source']
    return service.update_category(id, source)


@category_blueprint.route("/", methods=['DELETE'])
def delete_category():
    json = request.json
    id = json['id']
    res = service.delete_category(id)
    if session.get('current_session', 1) == id:  # TODO - сессия всегда должна быть известна
        session['current_category'] = 1
        session.modified = True
    return res
