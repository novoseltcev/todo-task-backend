#
#
#
from server.crud.locale import flask_app, request, handler_category as hnd


@flask_app.route("/category", methods=['GET'])
def open_category():
    json = request.json
    id_category = json['id_category']
    return hnd.open_category(id_category)


@flask_app.route("/category", methods=['POST'])
def create_category():
    json = request.json
    name_category = json["name_category"]
    return hnd.create_category(name_category)


@flask_app.route("/category", methods=['PUT'])
def edit_category():
    json = request.json
    destination_id = json['id_category']
    source = json['source']
    return hnd.update_category(destination_id, source)


@flask_app.route("/category", methods=['DELETE'])
def delete_category():
    json = request.json
    id_category = json['id_category']
    return hnd.delete_category(id_category)
