from sqlite3 import IntegrityError
from server.crud import rerender_page
from sqlite_db import SQLiteDB


def create_task(db: SQLiteDB, task_name):
    db.append_task(task_name)
    return rerender_page(), 202


def create_category(db: SQLiteDB, category_name):
    try:
        db.append_category(category_name)
        db.current_category = category_name
        return rerender_page(), 202

    except IntegrityError:
        return {"error": "value already exists"}, 400


def update_task_status(db: SQLiteDB, task_id: int, new_status: int):
    db.update_task_status(task_id, new_status)  # TODO
    return rerender_page, 204


def update_task_category(db: SQLiteDB, task_id: int, new_category_id: int):
    db.update_task_category(task_id, new_category_id)
    return rerender_page, 204


def update_category(db: SQLiteDB, destination, source_id: int):
    db.rename_category(destination, source_id)


def delete_task(db: SQLiteDB, task_id: int):
    db.remove_task(task_id)


def delete_category(db: SQLiteDB, category_id: int):
    db.remove_category(category_id)
