from flask import send_file
from os import remove
from server.crud.locale import rerender_page, DB, files_path


def download_file(id_file: int):
    DB.assert_file(id_file)
    id_file_1, filename, path, id_task = DB.get_file(id_file)
    result = send_file(files_path + filename)
    return result


def create_file(filename: str, data, id_task: int):
    DB.assert_task(id_task)
    path = 'server/' + files_path + filename
    with open(path, "wb+") as fp:
        fp.write(data)

    DB.insert_file(filename, path, id_task)
    return rerender_page(), 201


def delete_file(id_file: int, path: str):
    DB.assert_file(id_file)
    DB.delete_file(id_file)
    remove(path)
    return rerender_page(), 202
