from app import create_app
from app.db import db


def main(dump_file='dumps/inserts.sql'):
    app = create_app()
    db.drop_all()
    db.create_all()

    with open(dump_file) as f:
        db.engine.execute(f.read())

    return app


if __name__ == '__main__':
    main()
