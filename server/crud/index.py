from server.crud.locale import rerender_page, flask_app


@flask_app.route("/", methods=["GET"])
def get_page():
    return rerender_page()
