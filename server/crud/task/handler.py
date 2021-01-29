from server.crud.locale import rerender_page, DB, current_category


def create_task(name_task):
    DB.insert_task(name_task, current_category.id)
    return rerender_page(), 201


def update_task(id_task: int, title: str, status: int, id_category: int):
    DB.assert_task(id_task)
    DB.assert_category(id_category)
    DB.update_task(id_task, title, status, id_category)
    return rerender_page(), 202


def delete_task(id_task: int):
    DB.assert_task(id_task)
    #DB.assert_file(id_file)
    #answer = DB.delete_file(id_file)
    DB.delete_task(id_task)
    return rerender_page(), 202
