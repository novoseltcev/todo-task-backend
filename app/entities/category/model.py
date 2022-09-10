from app.db import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    name = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=True)

    tasks = db.relationship('Task', order_by='Task.id', lazy=True, cascade='all,delete')
