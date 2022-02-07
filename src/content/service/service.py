from typing import Optional, ByteString
from datetime import datetime

from ..domain import model
from . import unit_of_work


def get_category(
    category_ref: str,
    actor_ref: str, uow: unit_of_work.AbstractUnitOfWork
) -> model.Category:
    with uow:
        category = uow.categories.get(category_ref)
        category.check_actor(model.ContentOwner(actor_ref))
        return category


def add_category(
    name: str, color: Optional[str],
    actor_ref: str, uow: unit_of_work.AbstractUnitOfWork
) -> str:
    with uow:
        category = model.Category(
            name=name,
            color=color,
            owner=model.ContentOwner(actor_ref)
        )
        uow.categories.add(category)
        uow.commit()
        return category.reference


def add_task(
    title: str, desc: Optional[str], deadline: Optional[datetime], status: str,
    category_ref: str, actor_ref: str, uow: unit_of_work.AbstractUnitOfWork
) -> str:
    with uow:
        category = uow.categories.get(category_ref)
        category.check_actor(model.ContentOwner(actor_ref))
        task = model.Task(
            title=title,
            status=model.Status(status),
            description=desc,
            deadline=deadline
        )
        category.tasks.append(task)
        uow.commit()
        return task.reference


def pin_file(
    filename: str, data: ByteString, task_ref: str,
    actor_ref: str, uow: unit_of_work.AbstractUnitOfWork
) -> str:
    with uow:
        category = uow.categories.get_by_task(task_ref)
        category.check_actor(model.ContentOwner(actor_ref))
        path = uow.storage.send(filename, data)
        file = model.File(
            filename=filename,
            external_path=path
        )
        task = next(task for task in category.tasks if task.reference == task_ref)
        task.files.append(file)
        uow.commit()
        return file.reference


def delete_category(
    category_ref: str,
    actor_ref: str, uow: unit_of_work.AbstractUnitOfWork
) -> None:
    with uow:
        category = uow.categories.get(category_ref)
        category.check_actor(model.ContentOwner(actor_ref))
        uow.categories.delete(category)
        uow.commit()


def delete_task(
    task_ref: str,
    actor_ref: str, uow: unit_of_work.AbstractUnitOfWork
) -> None:
    with uow:
        category = uow.categories.get_by_task(task_ref)
        category.check_actor(model.ContentOwner(actor_ref))
        task = next(task for task in category.tasks if task.reference == task_ref)
        category.tasks.remove(task)
        uow.commit()


def unpin_file(
    file_ref: str, task_ref: str,
    actor_ref: str, uow: unit_of_work.AbstractUnitOfWork
) -> None:
    with uow:
        category = uow.categories.get_by_file(file_ref)
        category.check_actor(model.ContentOwner(actor_ref))
        task = next(task for task in category.tasks if task.reference == task_ref)
        file = next(file for file in task.files if file.reference == file_ref)
        uow.storage.delete(file.external_path)
        task.files.remove(file)
        uow.commit()


def update_category(
    category_ref: str,
    new_name: str, new_color: str,
    actor_ref: str, uow: unit_of_work.AbstractUnitOfWork
) -> None:
    with uow:
        category = uow.categories.get(category_ref)
        category.check_actor(model.ContentOwner(actor_ref))
        category.name = new_name
        category.color = new_color
        uow.commit()


def update_task(
    task_ref: str,
    new_title: str, new_desc: Optional[str], new_deadline: Optional[datetime], new_status: str,
    actor_ref: str, uow: unit_of_work.AbstractUnitOfWork
) -> None:
    with uow:
        category = uow.categories.get_by_task(task_ref)
        category.check_actor(model.ContentOwner(actor_ref))
        task = next(task for task in category.tasks if task.reference == task_ref)
        task.title = new_title
        task.description = new_desc
        task.deadline = new_deadline
        task.status = model.Status(new_status)
        uow.commit()


def move_task(
    task_ref: str, new_category_ref: str,
    actor_ref: str, uow: unit_of_work.AbstractUnitOfWork
) -> None:
    with uow:
        category = uow.categories.get_by_task(task_ref)
        category.check_actor(model.ContentOwner(actor_ref))
        new_category = uow.categories.get(new_category_ref)
        new_category.check_actor(category.owner)
        task = next(task for task in category.tasks if task.reference == task_ref)
        new_category.tasks.append(task)
        category.tasks.remove(task)
        uow.commit()
