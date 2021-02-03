from flask import render_template, session
from server.initialize_db import engine
from server.task.repository import task_rep, file_rep
from server.category.repository import category_rep


def rerender_page():
    try:
        session['current_category']
    except KeyError:
        pass
        # session['current_category'] = 1

    current_category = session.get('current_category', 1)
    if current_category == 1:
        tasks = task_rep.get()
    else:
        try:
            tasks = task_rep.get_by_foreign(current_category)
        except ValueError as error:
            return error.args[0], 404

    categories = category_rep.get()
    files = file_rep.get()
    assert (len(categories) != 0)
    return render_template("index.html", tasks=tasks, categories=categories, files=files)

