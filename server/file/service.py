import os

from flask import send_file

from .repository import FileRepository
from .schema import FileSchema
from .serializer import serialize_file

from server.task.service import task_repository
from server import config


file_repository = FileRepository()
files_dir = config.UPLOAD_FOLDER
root_dir = config.ROOT


@file_repository.assert_id
def get_one(id: int):
    file = file_repository.get_by_primary(id)
    return serialize_file(file)


@file_repository.assert_id
def download(id: int):
    file = file_repository.get_by_primary(id)
    path = file.path
    name = file.name
    full_path = os.path.join(os.getcwd(), path)
    return send_file(full_path, attachment_filename=name, as_attachment=True)


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


def create(task: int, name: str, data):
    task_repository.get_by_primary(task)
    path = get_unique_path(name)
    file_repository.insert(name, path, task)
    with open(path, 'wb+') as fp:
        fp.write(data)


@file_repository.assert_id
def delete(id: int):
    path = file_repository.get_by_primary(id).path
    cwd = os.getcwd()
    full_path = os.path.join(cwd, path)

    os.remove(full_path)
    file_repository.delete(id)
