#
#
#
from server.handler.locale import error_handler, rerender_page, DB, id_current_category


@error_handler
def open_category(id_category: int):
    global id_current_category
    DB.assert_category(id_category)
    id_current_category = id_category
    return rerender_page()


@error_handler
def create_category(name_category):
    DB.insert_category(name_category)
    DB.current_category = name_category
    return rerender_page(), 201


@error_handler
def update_category(destination_id: int, source: str):
    DB.assert_category(destination_id)
    if destination_id == 1:
        raise ValueError("ban on changing the main category")
    DB.update_category_name(destination_id, source)
    return rerender_page(), 202


@error_handler
def delete_category(id_category: int):
    DB.assert_category(id_category)
    tasks = DB.get_filtered_tasks(id_category)
    for task in tasks:
        DB.delete_task(task['id_task'])

    DB.delete_category(id_category)
    return rerender_page(), 202
