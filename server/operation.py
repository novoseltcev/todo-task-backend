from sqlite3 import IntegrityError
from flask import render_template
from server.sqlite_db import SQLiteDB

global id_current_category


def rerender_page(db: SQLiteDB):
    global id_current_category
    try:
        id_current_category == 1
    except NameError:
        id_current_category = 1

    if id_current_category == 1:
        tasks = db.get_all_tasks()
    else:
        try:
            tasks = db.get_filtered_tasks(id_current_category)
        except ValueError:
            return raise_error()

    categories = db.get_categories()
    assert (len(categories) != 0)
    return render_template("index.html", tasks=tasks, categories=categories)


def open_category(db: SQLiteDB, id_category: int):
    global id_current_category
    try:
        db.is_exist_category(id_category)
        id_current_category = id_category
    except ValueError:
        pass

    db.current_id_category = id_category


def create_task(db: SQLiteDB, name_task):
    global id_current_category
    try:
        db.insert_task(name_task, id_current_category)
        return rerender_page(db), 201
    except ValueError:
        return raise_error()


def create_category(db: SQLiteDB, name_category):
    try:
        db.insert_category(name_category)
        db.current_category = name_category
        return rerender_page(db), 201
    except IntegrityError:
        return {"error": "value already exists"}, 400


def update_task_status(db: SQLiteDB, id_task: int, new_status: int):
    try:
        db.update_task_status(id_task, new_status)
        return rerender_page(db), 202
    except ValueError:
        return raise_error()


def update_task_category(db: SQLiteDB, id_task: int, new_id_category: int):
    try:
        db.update_task_category(id_task, new_id_category)
        return rerender_page(db), 202
    except ValueError:
        return raise_error()


def update_category_name(db: SQLiteDB, destination_id: int, source: str):
    try:
        db.update_category_name(destination_id, source)
        return rerender_page(db), 202
    except ValueError:
        return raise_error()


def delete_task(db: SQLiteDB, id_task: int):
    try:
        db.delete_task(id_task)
        return rerender_page(db), 202
    except ValueError:
        return raise_error()


def delete_category(db: SQLiteDB, id_category: int):
    try:
        db.delete_category(id_category)
        return rerender_page(db), 202
    except ValueError:
        return rerender_page(db)


def raise_error():
    return 404
