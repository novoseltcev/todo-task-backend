from flask import Blueprint


task_blueprint = Blueprint('task', __name__)
__all__ = ["controller", 'task_blueprint']
