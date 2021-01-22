#
#
#

from server.handler.locale import error_handler, rerender_page, DB
from os import remove
from flask import send_file


@error_handler
def download_file(id_file: int):
    DB.assert_file(id_file)
    filename, data = DB.get_file(id_file)
    with open("server/" + filename, "wb+") as fp:
        fp.write(data)

    result = send_file(filename)
    remove("server/" + filename)
    return result


@error_handler
def create_file(id_task: int, filename: str, data):
    DB.assert_task(id_task)
    DB.insert_file(filename, data)
    added_file_id = DB.get_files()
    DB.update_task_file(id_task, added_file_id[-1]['id_file'])
    return rerender_page(), 201


@error_handler
def delete_file(id_task: int, id_file: int):
    DB.assert_task(id_task)
    DB.assert_file(id_file)
    DB.delete_file(id_file)
    DB.update_task_file(id_task, 0)
    return rerender_page(), 202


