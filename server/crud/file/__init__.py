from flask import Blueprint


file_blueprint = Blueprint('file', __name__)
__all__ = ["route", 'file_blueprint']
