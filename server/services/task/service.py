from ._serviceABC import TaskService
from .schema import TaskSchema
from .response import TaskResponse
from .model import Task
from ._repositoryABC import Tasks


class TaskLogic(TaskService):
    @classmethod
    def get(cls, schema: TaskSchema) -> TaskResponse:
        task = Tasks.load(schema.id)
        assert task.id_user == schema.id_user  # TODO
        return TaskResponse.dump(task)

    @classmethod
    def get_all(cls, schema: TaskSchema) -> TaskResponse:
        tasks = Tasks.load_by_category(schema.id_category)
        if len(tasks) > 0:
            assert tasks[0].id_user == schema.id_user  # TODO
        return TaskResponse.dump(tasks, many=True)

    @classmethod
    def create(cls, schema: TaskSchema) -> TaskResponse:
        Tasks.check_category(schema.id_category)
        task = Task(id_user=schema.id_user, id_category=schema.id_category, title=schema.title, status=False)
        Tasks.save(task)
        return TaskResponse.success()

    @classmethod
    def edit_title(cls, schema: TaskSchema) -> TaskResponse:
        task = Tasks.load(schema.id)
        assert task.id_user == schema.id_user
        task.title = schema.title
        Tasks.save(task)
        return TaskResponse.success()

    @classmethod
    def change_status(cls, schema: TaskSchema) -> TaskResponse:
        task = Tasks.load(schema.id)
        assert task.id_user == schema.id_user
        task.title = not task.title
        Tasks.save(task)
        return TaskResponse.success()

    @classmethod
    def change_category(cls, schema: TaskSchema) -> TaskResponse:
        task = Tasks.load(schema.id)
        assert task.id_user == schema.id_user
        Tasks.check_category(schema.id_category)
        task.id_category = schema.id_category
        Tasks.save(task)
        return TaskResponse.success()

    @classmethod
    def delete(cls, schema: TaskSchema) -> TaskResponse:
        task_id = schema.id
        task = Tasks.load(task_id)
        assert task.id_user == schema.id_user
        Tasks.delete(task_id)
        return TaskResponse.success()
