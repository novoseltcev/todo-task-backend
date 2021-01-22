from sqlite3 import IntegrityError
from flask import render_template
from server import DB


id_current_category = 1


def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            return raise_error(error.args[0])
        except IntegrityError:
            return raise_error({"error": "value already exists"})

    return wrapper


def rerender_page():
    if id_current_category == 1:
        tasks = DB.get_all_tasks()
    else:
        try:
            tasks = DB.get_filtered_tasks(id_current_category)
        except ValueError as error:
            return raise_error(error.args[0])

    categories = DB.get_categories()
    files = DB.get_files()
    assert (len(categories) != 0)
    return render_template("index.html", tasks=tasks, categories=categories, files=files)


def raise_error(msg):
    return msg, 404
