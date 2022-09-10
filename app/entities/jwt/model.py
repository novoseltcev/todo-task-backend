from app.db import db


class JWTToken(db.Model):
    jti = db.Column(db.String, nullable=False, primary_key=True)
    revoked = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    end_life = db.Column(db.DateTime, nullable=False)
