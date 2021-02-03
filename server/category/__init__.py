from flask import Blueprint


category_blueprint = Blueprint('category', __name__)
__all__ = ["controller", 'category_blueprint']
