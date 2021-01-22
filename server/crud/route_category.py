#
#
#
from server.crud.locale import flask_app, preset_json_receive_method
from server.crud.locale import handler_category as hnd


@flask_app.route("/category", methods=['GET'])
#@preset_json_receive_method
def open_category(json):
    id_category = int(json['id_category'])
    return hnd.open_category(id_category)


@flask_app.route("/category", methods=['POST'])
#@preset_json_receive_method
def create_category(json):
    name_category = json["name_category"]
    return hnd.create_category(name_category)


@flask_app.route("/category", methods=['PUT'])
#@preset_json_receive_method
def edit_category(json):
    destination_id = int(json['id_category'])
    source = json['source']
    return hnd.update_category(destination_id, source)


@flask_app.route("/category", methods=['DELETE'])
#@preset_json_receive_method
def delete_category(json):
    id_category = int(json['id_category'])
    return hnd.delete_category(id_category)
