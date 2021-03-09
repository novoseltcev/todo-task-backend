from os import path, getcwd

from flask import send_from_directory

from server import app
from server import DB_session


@app.route("/")
def index():
    return send_from_directory(path.join(getcwd(), 'server', 'static', 'templates'), 'index.html')


@app.teardown_appcontext
def shutdown_session(exception=None):
    DB_session.remove()


def session_handler(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            DB_session.commit()
            return result
        except Exception as e:
            DB_session.rollback()
            raise e

    return wrapper
