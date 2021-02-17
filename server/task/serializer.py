# Серилазизация данных
from .schema import TaskSchema
from .model import Task


def get_task_json(task: Task):
    return TaskSchema().dump(task)

