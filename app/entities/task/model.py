from app.db import db


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    name = db.Column(db.String, nullable=False)
    status = db.Column(db.Boolean, default=False)

    files = db.relationship('File', order_by='File.uuid', lazy=True, cascade='all,delete')
