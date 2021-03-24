import os
from uuid import uuid4

from flask import send_file
from celery.result import AsyncResult

from server import s3_bucket, celery
from server.file.repository import FileRepository
from server.file.serializer import serialize_file, FileSchema

from server.task import service as task_service


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


@celery.task(name='s3_cloud.upload')
def s3_upload(path):
    s3_file = s3_bucket.Object(key=path)
    tmp_path = os.path.join(os.getcwd(), 'server', 'tmp', path)
    with open(tmp_path, 'rb') as fp:
        s3_file.upload_fileobj(fp)


def check_uploading(id_user, id, path, uuid):
    result = AsyncResult(uuid)
    if result.failed():
        FileRepository.delete(id_user, id)
        tmp_path = os.path.join(os.getcwd(), 'server', 'tmp', path)
        os.remove(tmp_path)

    if result.successful():
        tmp_path = os.path.join(os.getcwd(), 'server', 'tmp', path)
        os.remove(tmp_path)
    return result.status


def delete(id_user, id):
    file = FileRepository.delete(id_user, id)

    s3_file = s3_bucket.Object(key=file.path)
    s3_file.delete()
    return serialize_file(file)
