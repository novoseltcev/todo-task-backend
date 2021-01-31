from flask import request
from server.crud.category import handler as hnd, category_blueprint


@category_blueprint.route('/')
def open_category():
    json = request.json
    id_category = json['id_category']
    res = hnd.open_category(id_category)
    # TODO - change session['current_category'] = id_category
    return res


@category_blueprint.route("/", methods=['POST'])
def create_category():
    json = request.json
    name_category = json["name_category"]
    res = hnd.create_category(name_category)
    # TODO - session['current_category'] = category['name_category'].id
    return res


@category_blueprint.route("/", methods=['PUT'])
def edit_category():
    json = request.json
    destination_id = json['id_category']
    source = json['source']
    return hnd.update_category(destination_id, source)


@category_blueprint.route("/", methods=['DELETE'])
def delete_category():
    json = request.json
    id_category = json['id_category']
    res = hnd.delete_category(id_category)
    # TODO - if deleted_session equal a current_session then session['current_category'] = default
    return res
