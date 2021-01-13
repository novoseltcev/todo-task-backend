#
# определение user-case-запроса
# с компоновкой его базовыми запросами к обёртке БД
# а также обеспечение стабильного ответа сервера клиенту
#
from sqlite3 import IntegrityError
from flask import render_template
from server.sqlite_db import SQLiteDB

global id_current_category


def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            return raise_error(error.args[0])
        except IntegrityError:
            return raise_error({"error": "value already exists"})

    return wrapper


def rerender_page(db: SQLiteDB):
    global id_current_category
    try:
        if id_current_category == 1:
            pass
    except NameError:
        id_current_category = 1

    if id_current_category == 1:
        tasks = db.get_all_tasks()
    else:
        try:
            tasks = db.get_filtered_tasks(id_current_category)
        except ValueError as error:
            return raise_error(error.args[0])

    categories = db.get_categories()
    assert (len(categories) != 0)
    return render_template("index.html", tasks=tasks, categories=categories)


@error_handler
def open_category(db: SQLiteDB, id_category: int):
    global id_current_category
    db.is_exist_category(id_category)
    id_current_category = id_category
    return rerender_page(db)


@error_handler
def download_file(db: SQLiteDB, id_file: int):
    (filename, data) = db.get_file(id_file)
    answer = {
        "filename": filename,
        "data": data
    }
    return rerender_page(db), answer, 201


@error_handler
def create_task(db: SQLiteDB, name_task):
    global id_current_category
    db.insert_task(name_task, id_current_category)
    return rerender_page(db), 201


@error_handler
def create_file(db: SQLiteDB, id_task: int, filename: str, data):
    db.insert_file(filename, data)
    added_file_id = db.get_files()
    db.update_task_file(id_task, added_file_id[-1]['id_file'])
    return rerender_page(db), 201


@error_handler
def create_category(db: SQLiteDB, name_category):
    db.insert_category(name_category)
    db.current_category = name_category
    return rerender_page(db), 201


@error_handler
def update_task_status(db: SQLiteDB, id_task: int, new_status: int):
    db.update_task_status(id_task, new_status)
    return rerender_page(db), 202


@error_handler
def update_task_category(db: SQLiteDB, id_task: int, new_id_category: int):
    db.update_task_category(id_task, new_id_category)
    return rerender_page(db), 202


@error_handler
def update_category_name(db: SQLiteDB, destination_id: int, source: str):
    db.update_category_name(destination_id, source)
    return rerender_page(db), 202


@error_handler
def delete_task(db: SQLiteDB, id_task: int):
    db.delete_task(id_task)
    return rerender_page(db), 202


@error_handler
def delete_category(db: SQLiteDB, id_category: int):
    tasks = db.get_filtered_tasks(id_category)
    for task in tasks:
        db.delete_task(task['id_task'])
    db.delete_category(id_category)
    return rerender_page(db), 202


@error_handler
def delete_file(db: SQLiteDB, id_task: int, id_file: int):
    db.delete_file(id_file)
    db.update_task_file(id_task, 0)
    return rerender_page(db), 202


def raise_error(msg):
    return msg, 404
