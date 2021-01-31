from server.local import flask_app
from server.crud.task import task_blueprint
from server.crud.category import category_blueprint
from server.crud.file import file_blueprint


flask_app.register_blueprint(task_blueprint, url_prefix="/task")
flask_app.register_blueprint(category_blueprint, url_prefix="/category")
flask_app.register_blueprint(file_blueprint, url_prefix="/file")
