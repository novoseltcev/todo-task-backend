from server.crud.bind_flask import flask_app
from server.crud.locale import rerender_page


@flask_app.route("/", methods=["GET"])
def get_page():
    return rerender_page()
