from flask import request
from server.category import service, category_blueprint
from flask import session


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
    if session.get('current_session') == id_category:
        session['current_category'] = 1
    return res
