from celery import Celery
from server import Config


def make_celery(flask_app):
    celery_app = Celery(flask_app.name,
                        broker=flask_app.config['CELERY_BROKER_URL'],
                        backend=Config.backend_result
                        )

    celery_app.conf.task_routes = {
        's3_cloud.*': {'queue': 's3'},
        # 'email.*': {'queue': 'email'}
    }

    task_base = celery_app.Task

    class ContextTask(task_base):
        abstract = True

        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return task_base.__call__(self, *args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app
