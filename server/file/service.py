import os
from flask import send_file
from server.file.serializer import File, engine
from server.file.repository import FileRepository
from server.task import service as svc


file_rep = FileRepository(engine, File)
files_dir = os.path.join('data', 'files')
root_dir = 'server'


def download_file(id: int):
    file_rep.assert_exist(id)
    path = file_rep.get_by_primary(id).path
    cwd = os.getcwd()
    result = send_file(os.path.join(cwd, path))
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


def create_file(name: str, data, task: int):
    svc.task_rep.assert_exist(task)
    path = get_unique_path(name)
    file_rep.insert(name, data, task, path)
    return svc.rerender_page(), 201


def delete_file(id: int):
    file_rep.assert_exist(id)

    path = file_rep.get_by_primary(id).path
    cwd = os.getcwd()
    full_path = os.path.join(cwd, path)
    os.remove(full_path)

    file_rep.delete(id)
    return svc.rerender_page(), 202
