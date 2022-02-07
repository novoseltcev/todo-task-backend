from datetime import date

from .. import Task


def generate_task(identity: int, category_id: int, account_id: int) -> Task:
        return Task(
            f'Task<{identity}>',
            'bla-bla-bla',
            date.fromisocalendar(2023, 1, 1),
            category_id,
            account_id,
            identity
        )
