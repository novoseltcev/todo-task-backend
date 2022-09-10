from app import create_app
from app.db import db


def main():
    create_app()
    db.drop_all()


if __name__ == '__main__':
    main()
