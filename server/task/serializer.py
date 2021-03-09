# Серилазизация данных
from server.task.schema import TaskSchema
from server.task.model import Task


def serialize_task(task: Task, many=False):
    return TaskSchema(many=many).dump(task)
