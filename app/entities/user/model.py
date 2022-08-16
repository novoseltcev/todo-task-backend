from enum import Enum, auto

from app.db import db


class Role(Enum):
    common = auto
    admin = auto


class Status(Enum):
    common = auto
    blocked = auto
    unconfirmed = auto


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.Date, nullable=False, server_default=db.text('now()'))
    role = db.Column(db.Enum(Role), default=Role.common)
    status = db.Column(db.Enum(Status), default=Status.unconfirmed)
    confirmation_token = db.Column(db.String, nullable=True)

    categories = db.relationship('Category', order_by='Category.id', lazy=True)
