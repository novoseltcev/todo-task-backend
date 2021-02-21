# Серилазизация данных
from .schema import TaskSchema
from .model import Task


def serialize_task(task: Task, many=False):
    return TaskSchema(many=many).dump(task)
