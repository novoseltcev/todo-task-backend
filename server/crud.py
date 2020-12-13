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
    if not app.update_task_status(json_request):
        if not app.update_task_category(json_request):
            if not app.update_category(json_request):
                abort(400)
    return rerender_page()


@app.route("/", methods=['DELETE'])
def delete():
    json_request = request.json
    if not app.delete_task(json_request):
        if not app.delete_category(json_request):
            abort(400)
    return rerender_page(), 205


def rerender_page():
    tasks, categories = app.get_data()
    return render_template("new_index.html", tasks=tasks, categories=categories)


