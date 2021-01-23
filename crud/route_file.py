#
#
#
from crud.locale import handler_file as hnd, flask_app, request


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
        data = file.read()
        return hnd.create_file(id_task, filename, data)


@flask_app.route("/file", methods=['DELETE'])
def delete_file():
    json = request.json
    id_task = json['id_task']
    id_file = json['id_file']
    return hnd.delete_file(id_task, id_file)
