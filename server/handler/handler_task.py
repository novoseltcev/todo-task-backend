#
#
#
from server.handler.locale import error_handler, rerender_page, DB, id_current_category


@error_handler
def create_task(name_task):
    DB.insert_task(name_task, id_current_category)
    return rerender_page(), 201


@error_handler
def update_task(id_task: int, title: str, status: int, id_category: int):
    DB.assert_task(id_task)
    DB.assert_category(id_category)
    DB.update_task(id_task, title, status, id_category)
    return rerender_page(), 202


@error_handler
def delete_task(id_task: int, id_file: int):
    DB.assert_task(id_task)
    DB.assert_file(id_file)
    answer = DB.delete_file(id_task, id_file)
    DB.delete_task(id_task)
    return answer
