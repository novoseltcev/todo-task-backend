from server import app
from flask import request, render_template, abort


@app.route("/", methods=['POST'])
def create_or_open_category():
    json_request = request.json
    if not app.create_task(json_request):
        if not app.create_category(json_request):
            if not app.open_category(json_request):
                abort(400)
            else:
                return rerender_page(), 200
    return rerender_page(), 201


@app.route("/", methods=['PUT'])
def update():
    json_request = request.json
    if not update_task_status(json_request):
        if not update_task_category(json_request):
            if not update_category(json_request):
                abort(400)
    return rerender_page()


@app.route("/", methods=['DELETE'])
def delete():
    json_request = request.json
    if not delete_task(json_request):
        if not delete_category(json_request):
            abort(400)
    return rerender_page(), 205


def rerender_page():
    filtered_db = app.db.copy()
    filtered_db.filter()
    return render_template("new_index.html", tasks=reversed(filtered_db.dictionary))


def create_task(json):
    if 'title' in json:
        task_title = json['title']
        app.db.append(task_title)
        return True
    return False


def create_category(json):
    if 'category' in json and json.get('operation') == 'create':
        task_category = json['category']
        app.db.append_category(task_category)
        return True
    return False


def open_category(json):
    if 'category' in json and json.get('operation') == 'open':
        app.db.current_category = json['category']
        return True
    return False


def update_task_status(json):
    if 'id' in json and 'category' not in json:
        task_id = json['id']
        app.db.change_status(task_id)
        return True
    return False


def update_task_category(json):
    if 'id' in json and 'category' in json:
        task_id = json['id']
        category_name = json['category']
        app.db.change_category(task_id, category_name)
        return True
    return False


def update_category(json):
    if 'destination_category' in json and 'source_category' in json:
        destination = json['destination_category']
        source = json['source_category']
        app.db.rename_category(destination, source)
        print("Done_u_C")
        return True
    return False


def delete_task(json):
    if 'id' in json:
        task_id = json['id']
        app.db.remove(task_id)
        return True
    return False


def delete_category(json):
    if 'category' in json:
        category_name = json['category']
        app.db.remove_by_category(category_name)
        return True
    return False
