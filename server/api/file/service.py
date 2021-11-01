import os
from uuid import uuid4

from flask import send_file
from celery.result import AsyncResult
from sqlalchemy.event import listens_for

from server import s3_bucket
from server.api.file.repository import FileRepository, File
from server.api.file.serializer import serialize_file

from server.api.task import service as task_service


def get_file(id_user, id):
    file = FileRepository.get_by_id(id_user, id)
    path = file.path
    name = file.name
    id_task = file.id_task
    return {'name': name, 'path': path, 'id_task': id_task}


def s3_download(name, path):
    s3_file = s3_bucket.Object(key=path)
    tmp_path = os.path.join(os.getcwd(), 'server', 'tmp', path)
    with open(tmp_path, 'wb') as data:
        s3_file.download_fileobj(data)

    result = send_file(tmp_path, attachment_filename=name, as_attachment=True)

    # os.remove(tmp_path)  # TODO
    return result


def generate_path(name):
    path = str(uuid4()) + os.path.splitext(name)[-1]
    return path


def create(id_user, id_task, name, path, data):
    task_service.get(id_user, id_task)
    id = FileRepository.insert(id_user, name, path, id_task).id

    tmp_path = os.path.join(os.getcwd(), 'server', 'tmp', path)
    with open(tmp_path, 'wb') as fp:
        fp.write(data)
    return id


def check_uploading(id_user, id, path, uuid):
    result = AsyncResult(uuid)
    tmp_path = os.path.join(os.getcwd(), 'server', 'tmp', path)
    if result.failed():
        FileRepository.delete(id_user, id)

    if result.successful() or result.failed():
        os.remove(tmp_path)

    return result.status


@listens_for(File, 'before_delete')
def clear_s3_bucket(mapper, connection, target):
    s3_file = s3_bucket.Object(key=target.path)
    s3_file.delete()


def delete(id_user, id):
    file = FileRepository.delete(id_user, id)
    return serialize_file(file)
