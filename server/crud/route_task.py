#
#
#
from server.crud.locale import flask_app, preset_json_receive_method
from server.crud.locale import handler_task as hnd


@flask_app.route("/task", methods=['POST'])
@preset_json_receive_method
def create_task(json):
    name_task = json["name_task"]
    return hnd.create_task(name_task)


@flask_app.route("/task", methods=['PUT'])
#@preset_json_receive_method
def edit_task(json):
    id_task = int(json['id_task'])
    title = json['title']
    status = int(json['status'])
    id_category = int(json['id_category'])
    return hnd.update_task(id_task, title, status, id_category)


@flask_app.route("/task", methods=['DELETE'])
#@preset_json_receive_method
def delete_task(json):
    id_task = int(json['id_task'])
    id_file = int(json['id_file'])
    return hnd.delete_task(id_task, id_file)

