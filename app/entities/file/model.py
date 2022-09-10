from app.db import db
from sqlalchemy.dialects.postgresql import UUID, dialect as pg_dialect

db.UUID = db.String

if db.engine.dialect.name == pg_dialect.name:
    db.UUID = UUID(as_uuid=True)


class File(db.Model):
    __tablename__ = 'files'

    uuid = db.Column(db.UUID, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    filename = db.Column(db.String, nullable=False)
    path = db.Column(db.String, unique=True, nullable=True)
