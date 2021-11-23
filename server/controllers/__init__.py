from flask import Blueprint

from .category import category_blueprint
from .task import task_blueprint
from .file import file_blueprint
from .user import user_blueprint
from .mail import mail_blueprint

api_blueprint = Blueprint("api", __name__, url_prefix="/api")
api_blueprint.register_blueprint(category_blueprint)
api_blueprint.register_blueprint(task_blueprint)
api_blueprint.register_blueprint(file_blueprint)
api_blueprint.register_blueprint(category_blueprint)
api_blueprint.register_blueprint(user_blueprint)
api_blueprint.register_blueprint(mail_blueprint)

__all__ = [
    'api_blueprint'
]
