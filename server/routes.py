def create_routes(flask_app):
    from server.email import email_blueprint
    from server.errors.handler import error_blueprint
    from server.views import view_blueprint
    from server.user import user_blueprint
    from server.category import category_blueprint
    from server.task import task_blueprint
    from server.file import file_blueprint

    flask_app.register_blueprint(email_blueprint)
    flask_app.register_blueprint(error_blueprint)
    flask_app.register_blueprint(view_blueprint)
    flask_app.register_blueprint(task_blueprint)
    flask_app.register_blueprint(category_blueprint)
    flask_app.register_blueprint(file_blueprint)
    flask_app.register_blueprint(user_blueprint)
