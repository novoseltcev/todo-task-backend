from flask import request, session
from server.category import service
from flask import Blueprint


category_blueprint = Blueprint('category', __name__)


@category_blueprint.route('/')
def open_category():
    json = request.json
    id_category = json['id_category']
    res = service.open_category(id_category)
    session['current_category'] = id_category
    session.modified = True
    return res


@category_blueprint.route("/", methods=['POST'])
def create_category():
    json = request.json
    name_category = json["name_category"]
    res = service.create_category(name_category)
    session['current_category'] = 1
    session.modified = True
    return res


@category_blueprint.route("/", methods=['PUT'])
def edit_category():
    json = request.json
    destination_id = json['id_category']
    source = json['source']
    return service.update_category(destination_id, source)


@category_blueprint.route("/", methods=['DELETE'])
def delete_category():
    json = request.json
    id_category = json['id_category']
    res = service.delete_category(id_category)
    if session.get('current_session', 1) == id_category:
        session['current_category'] = 1
        session.modified = True
    return res
