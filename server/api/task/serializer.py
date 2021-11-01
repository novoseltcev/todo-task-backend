from server.api.task.schema import TaskSchema
from server.api.task.model import Task


def serialize_task(task: Task, many=False):
    return TaskSchema(many=many).dump(task)
