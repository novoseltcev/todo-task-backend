from flask import request
from server.crud.category import handler as hnd, category_blueprint


@category_blueprint.route('/', methods=['GET'])
def open_category():
    json = request.json
    id_category = json['id_category']
    return hnd.open_category(id_category)


@category_blueprint.route("/", methods=['POST'])
def create_category():
    json = request.json
    name_category = json["name_category"]
    return hnd.create_category(name_category)


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
    return hnd.delete_category(id_category)
