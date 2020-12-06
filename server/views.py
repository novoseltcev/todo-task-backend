from server.crud import app, rerender_page


@app.route("/")
def index():
    return rerender_page(), 200

