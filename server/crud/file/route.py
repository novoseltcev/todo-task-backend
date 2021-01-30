from server.crud.locale import flask_app, request
from server.crud.file import handler as hnd


@flask_app.route("/get-file", methods=['POST'])
def open_file():
    json = request.json
    if json is not None:
        id_file = json['id_file']
    else:
        id_file = request.form['id_file']
    return hnd.download_file(id_file)


@flask_app.route("/file", methods=['POST'])
def create_file():
    file = request.files['file']
    if file is not None:
        id_task = request.form["id_task"]
        filename = file.filename
        data = file.read()  # TODO  --  Выгрузка на диск
        return hnd.create_file(filename, data, id_task)


@flask_app.route("/file", methods=['DELETE'])
def delete_file():
    json = request.json
    id_file = json['id_file']
    path = json['path']
    return hnd.delete_file(id_file, path)
