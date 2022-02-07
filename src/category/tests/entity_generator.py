from .. import Category


def generate_category(identity: int, account: int) -> Category:
    return Category(
        identity=identity,
        name=f'Category<{identity}>',
        account=account
    )
