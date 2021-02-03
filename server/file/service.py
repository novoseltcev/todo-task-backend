from flask import send_file
from server.locale import rerender_page
from server.file.repository import file_rep
from server.file.model import File
from server.file import schema
from server.task.repository import task_rep
from server.file import serializer


def download_file(id_file: int):
    file_rep.assert_existfile(id_file)
    id_file_1, filename, path, id_task = file_rep.get_by_primary(id_file)
    file = File(filename, path)
    result = send_file(file.get_full_path())
    return result


def create_file(filename: str, data, id_task: int):
    task_rep.assert_exist(id_task)
    path = schema.validate_path(filename)
    file = File(filename, path)
    file.save(data)
    file_rep.insert(filename, path, id_task)
    return rerender_page(), 201


def delete_file(id_file: int):
    file_rep.assert_exist(id_file)
    file_rep.delete(id_file)
    return rerender_page(), 202
