from __future__ import annotations
from typing import Tuple

from .schema import TaskSchema
from .model import Task


class TaskResponse(dict):
    @staticmethod
    def dump(task: Task | Tuple[Task], many=False):
        return TaskResponse(TaskSchema(many=many).dump(task))

    @staticmethod
    def success():
        return TaskResponse(success=True)
