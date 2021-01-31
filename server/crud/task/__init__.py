from flask import Blueprint


task_blueprint = Blueprint('task', __name__)
__all__ = ["route", 'task_blueprint']
