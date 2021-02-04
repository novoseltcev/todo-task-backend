import os
from flask import send_file
from server.file.serializer import File, engine
from server.file.repository import FileRepository
from server.task import service as svc


file_rep = FileRepository(engine, File)


def download_file(id_file: int):
    file_rep.assert_existfile(id_file)
    id_file_1, filename, path, id_task = file_rep.get_by_primary(id_file)
    file = File(filename, path)
    result = send_file(file.get_full_path())
    return result


def create_file(filename: str, data, id_task: int):
    svc.task_rep.assert_exist(id_task)
    path = os.path.join(os.getcwd(), 'server', 'data', 'files', filename)  # TODO
    print(path)
    # path = schema.validate_path(filename)
    # file = File(filename, path)
    # file.save(data)
    file_rep.insert(filename, path, id_task)
    return svc.rerender_page(), 201


def delete_file(id_file: int):
    file_rep.assert_exist(id_file)
    file_rep.delete(id_file)
    return svc.rerender_page(), 202
