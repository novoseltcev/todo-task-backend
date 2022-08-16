from app.db import db


class Category(db.Model):
    __tablename__ = 'categories'

    user_id = db.ForeignKey(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)

    pk = db.PrimaryKeyConstraint(user_id, name)
