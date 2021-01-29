from server.crud.locale import rerender_page, DB, current_category


def open_category(id_category: int):
    DB.assert_category(id_category)
    current_category.id = id_category
    return rerender_page()


def create_category(name_category):
    DB.insert_category(name_category)
    DB.current_category = name_category
    return rerender_page(), 201


def update_category(destination_id: int, source: str):
    DB.assert_category(destination_id)
    if destination_id == 1:
        raise ValueError("ban on changing the main category")
    DB.update_category(destination_id, source)
    return rerender_page(), 202


def delete_category(id_category: int):
    DB.assert_category(id_category)
    tasks = DB.get_filtered_tasks(id_category)
    for task in tasks:
        DB.delete_task(task['id_task'])

    DB.delete_category(id_category)
    return rerender_page(), 202
