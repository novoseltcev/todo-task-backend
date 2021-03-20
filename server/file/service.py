import os
from uuid import uuid4

from flask import send_file

from server import celery, s3_bucket
from server.file.repository import FileRepository
from server.file.serializer import serialize_file, FileSchema

from server.task.service import TaskRepository


def get_path(id_user, id):
    return FileRepository.get_by_id(id_user, id).path


@celery.task(name='cloud_s3.download')
def download(id_user, id):
    file = FileRepository.get_by_id(id_user, id)
    path = file.path
    name = file.name

    s3_file = s3_bucket.Object(key=path)
    tmp_path = os.path.join('tmp', path)
    with open(tmp_path, 'wb') as data:
        s3_file.download_fileobj(data)

    result = send_file(tmp_path, attachment_filename=name, as_attachment=True)

    os.remove(tmp_path)
    return result


# @celery.task(name='cloud_s3.upload')
def upload(id_user, id_task, name: str, data):
    TaskRepository.get_by_id(id_user, id_task)
    path = str(uuid4()) + os.path.splitext(name)[-1]
    file = FileRepository.insert(id_user, name, path, id_task)

    s3_file = s3_bucket.Object(key=path)
    tmp_path = os.path.join(os.getcwd(), 'server', 'tmp', path)
    print(tmp_path)
    with open(tmp_path, 'wb') as fp:
        fp.write(data)

    with open(tmp_path, 'rb') as fp:
        s3_file.upload_fileobj(fp)

    os.remove(tmp_path)
    return file.path


@celery.task(name='cloud_s3.delete')
def delete(id_user, id):
    path = FileRepository.get_by_id(id_user, id).path

    s3_file = s3_bucket.Object(key=path)
    s3_file.delete()

    file = FileRepository.delete(id_user, id)
    return serialize_file(file)
