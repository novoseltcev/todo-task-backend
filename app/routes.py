from flask import Flask

from app.entities.task.controller import TaskController
from app.entities.category.controller import CategoryController
from app.entities.file.controller import FileController, FileUploadingController
from app.entities.jwt.controller import JWTController
from app.entities.user.controller import UserController


def register_routes(app: Flask):
    api_prefix = ''

    user_view = UserController.as_view('user')
    app.add_url_rule(api_prefix + '/user', view_func=user_view)

    jwt_view = JWTController.as_view('jwt')
    app.add_url_rule(api_prefix + '/jwt', view_func=jwt_view)

    task_view = TaskController.as_view('task')
    app.add_url_rule(api_prefix + '/tasks', view_func=task_view)
    app.add_url_rule(api_prefix + '/tasks/<int:task_id>', view_func=task_view)

    category_view = CategoryController.as_view('category')
    app.add_url_rule(api_prefix + '/categories', view_func=category_view)
    app.add_url_rule(api_prefix + '/categories/<int:category_id>', view_func=category_view)

    file_view = FileController.as_view('file')
    app.add_url_rule(api_prefix + '/files', view_func=file_view)
    app.add_url_rule(api_prefix + '/files/<int:file_id>', view_func=file_view)

    file_uploading_view = FileUploadingController.as_view('file_uploading')
    app.add_url_rule(api_prefix + '/files/status/<uuid:token>', view_func=file_uploading_view)
