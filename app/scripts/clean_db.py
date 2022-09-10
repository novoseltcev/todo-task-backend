from app import create_app
from app.db import db


def main():
    create_app()
    for tbl in reversed(db.metadata.sorted_tables):
        db.engine.execute(tbl.delete())


if __name__ == '__main__':
    main()
