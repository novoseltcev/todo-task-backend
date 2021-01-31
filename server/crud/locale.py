from flask import render_template
from server.local import DB


class Category:  # TODO - delete class
    id = 1


def rerender_page():  # TODO - add new param: current_category
    if current_category.id == 1:
        tasks = DB.get_all_tasks()
    else:
        try:
            tasks = DB.get_filtered_tasks(current_category.id)
        except ValueError as error:
            return error.args[0], 404

    categories = DB.get_categories()
    files = DB.get_files()
    assert (len(categories) != 0)
    return render_template("index.html", tasks=tasks, categories=categories, files=files)


current_category = Category()  # TODO - delete init
files_path = "data/files/"
