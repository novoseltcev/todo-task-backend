import os

from flask import send_file

from .repository import FileRepository
from .schema import FileSchema
from .serializer import serialize_file

from server.task import service as t_svc
from server.initialize_db import config


file_rep = FileRepository()
files_dir = config.UPLOAD_FOLDER
root_dir = config.ROOT


@file_rep.assert_kwargs
def download_file(**kwargs):
    file = file_rep.get_by_primary(**kwargs)
    path = file.path
    name = file.name
    cwd = os.getcwd()
    return send_file(os.path.join(cwd, path), attachment_filename=name, as_attachment=True)


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

    t_svc.task_rep.assert_exist(task)
    path = get_unique_path(name)
    file_rep.insert(name, path, task)
    with open(path, 'wb+') as fp:
        fp.write(data)


@file_rep.assert_kwargs
def delete_file(**kwargs):
    path = file_rep.get_by_primary(**kwargs).path
    cwd = os.getcwd()
    full_path = os.path.join(cwd, path)
    os.remove(full_path)

    file_rep.delete(**kwargs)
