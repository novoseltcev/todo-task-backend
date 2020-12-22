from sqlite3 import IntegrityError
from flask import render_template
from server.sqlite_db import SQLiteDB


def rerender_page(db: SQLiteDB):
    categories = db.get_categories()
    if db.current_id_category == 1:
        tasks = db.get_all_tasks()
    else:
        tasks = db.get_filtered_tasks(db.current_id_category)
    #assert (len(categories) != 0)
    return render_template("index.html", tasks=tasks, categories=categories)


def create_task(db: SQLiteDB, name_task):
    db.insert_task(name_task)
    return rerender_page(db), 201


def create_category(db: SQLiteDB, name_category):
    try:
        db.insert_category(name_category)
        db.current_category = name_category
        return rerender_page(db), 201
    except IntegrityError:
        return {"error": "value already exists"}, 400


def update_task_status(db: SQLiteDB, task_id: int, new_status: int):
    db.update_task_status(task_id, new_status)
    return rerender_page(db), 202


def update_task_category(db: SQLiteDB, task_id: int, new_category_id: int):
    db.update_task_category(task_id, new_category_id)
    return rerender_page(db), 202


def update_category_name(db: SQLiteDB, destination_id: int, source: str):
    db.update_category_name(destination_id, source)
    return rerender_page(db), 202


def delete_task(db: SQLiteDB, task_id: int):
    db.delete_task(task_id)
    return rerender_page(db), 204


def delete_category(db: SQLiteDB, category_id: int):
    db.delete_category(category_id)
    return rerender_page(db), 204


def raise_error():
    return 404
