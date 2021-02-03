from server.app import app
from server.locale import rerender_page


@app.route("/")
def get_page():
    return rerender_page()
