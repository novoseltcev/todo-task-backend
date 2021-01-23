#
#
#
from crud.locale import handler_task as hnd, flask_app, request


@flask_app.route("/task", methods=['POST'])
def create_task():
    json = request.json
    name_task = json["name_task"]
    return hnd.create_task(name_task)


@flask_app.route("/task", methods=['PUT'])
def edit_task():
    json = request.json
    id_task = json['id_task']
    title = json['title']
    status = json['status']
    id_category = json['id_category']
    return hnd.update_task(id_task, title, status, id_category)


@flask_app.route("/task", methods=['DELETE'])
def delete_task():
    json = request.json
    id_task = json['id_task']
    #id_file = int(json['id_file'])
    return hnd.delete_task(id_task)
