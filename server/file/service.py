import os
from uuid import uuid4

from flask import send_file

from server.file.repository import FileRepository
from server.file.serializer import serialize_file, FileSchema

from server.task.service import TaskRepository
from server import config


files_dir = config.UPLOAD_FOLDER
root_dir = config.ROOT


def get_one(id: int):
    file = FileRepository.get_by_id(id)
    return serialize_file(file)


def download(id: int):
    file = FileRepository.get_by_id(id)
    path = file.path
    name = file.name
    full_path = os.path.join(os.getcwd(), path)
    return send_file(full_path, attachment_filename=name, as_attachment=True)


def create(task_id: int, name: str, data):
    TaskRepository.get_by_id(task_id)
    path = str(uuid4())
    file = FileRepository.insert(name, path, task_id)
    with open(path, 'wb+') as fp:
        fp.write(data)
    return file.id


def delete(id: int):
    path = FileRepository.get_by_id(id).path
    full_path = os.path.join(os.getcwd(), path)

    os.remove(full_path)
    file = FileRepository.delete(id)
    return serialize_file(file)
