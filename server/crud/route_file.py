#
#
#
from server.crud.locale import request, flask_app, preset_json_receive_method
from server.crud.locale import handler_file as hnd


@flask_app.route("/file", methods=['GET'])
#@preset_json_receive_method
def open_file(json):
    id_file = int(json['id_file'])
    return hnd.download_file(id_file)


@flask_app.route("/file", methods=['POST'])
def create_file():
    file = request.files.get('file')
    if file is not None:
        id_task = 1
        filename = file.filename
        data = file.read()
        return hnd.create_file(id_task, filename, data)


@flask_app.route("/file", methods=['DELETE'])
#@preset_json_receive_method
def delete_file():
    id_task = int(json['id_task'])
    id_file = int(json['id_file'])
    return hnd.delete_file(id_task, id_file)
