from app.db import db


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    status = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('categories.user_id', ondelete='CASCADE'), nullable=False)
    category_name = db.Column(db.Integer, db.ForeignKey('categories.name', ondelete='CASCADE'), nullable=False)

    files = db.relationship('File', order_by='File.name', lazy=True, cascade='all,delete')
