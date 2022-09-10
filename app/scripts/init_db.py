from app import create_app
from app.db import db


def main(insert_file="dumps/inserts.sql"):
    create_app()
    db.create_all()

    with open(insert_file) as fd:
        db.engine.execute(fd.read())


if __name__ == '__main__':
    main()
