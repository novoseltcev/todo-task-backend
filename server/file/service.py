import os

from flask import send_file, redirect, send_from_directory
from marshmallow import INCLUDE

from .repository import FileRepository
from .schema import FileSchema

from server.task import service as svc
from server.initialize_db import DB_config


file_rep = FileRepository()
files_dir = DB_config['UPLOAD_FOLDER']
root_dir = DB_config['ROOT']


def download_file(json):
    schema = FileSchema(only=('id',)).load(json)
    id = schema['id']

    file_rep.assert_exist(id)
    file = file_rep.get_by_primary(id)
    path = file.path
    name = file.name
    cwd = os.getcwd()
    result = send_file(os.path.join(cwd, path), attachment_filename=name, as_attachment=True)
    return result


def get_unique_path(name):
    files = tuple(os.walk(os.path.join(root_dir, files_dir)))[0][2]

    if name not in files:
        cur_name = name
    else:
        index = 1
        while True:
            cur_name = name + '(' + str(index) + ')'
            if cur_name not in files:
                break
            index = index + 1

    result = os.path.join(root_dir, files_dir, cur_name)

    return result


def create_file(json):
    schema = FileSchema(only=('name', 'task', 'data')).load(json)
    name = schema['name']
    task = schema['task']
    data = schema['data']

    svc.task_rep.assert_exist(task)
    path = get_unique_path(name)
    file_rep.insert(name, path, task)
    with open(path, 'wb+') as fp:
        fp.write(data)

    return redirect('/', 201)


def delete_file(json):
    schema = FileSchema(only=('id',)).load(json)
    id = schema['id']

    file_rep.assert_exist(id)

    path = file_rep.get_by_primary(id).path
    cwd = os.getcwd()
    full_path = os.path.join(cwd, path)
    os.remove(full_path)

    file_rep.delete(id)
    return redirect('/', 202)
