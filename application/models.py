from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

MAX_LENGTH = {
    'user_email': 40,
    'user_first_name': 20,
    'user_last_name': 20
}


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(
        db.String(MAX_LENGTH['user_email']),
        unique=True,
        nullable=False
        )
    first_name = db.Column(
        db.String(MAX_LENGTH['user_first_name']),
        nullable=False
        )
    last_name = db.Column(
        db.String(MAX_LENGTH['user_last_name']),
        nullable=False
        )
