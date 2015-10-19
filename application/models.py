from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from flask.ext.login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

db = SQLAlchemy()

MAX_LENGTH = {
    'email': 40,
    'first_name': 20,
    'last_name': 20
}


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(
        db.String(MAX_LENGTH['email']),
        unique=True,
        nullable=False
        )
    first_name = db.Column(
        db.String(MAX_LENGTH['first_name']),
        nullable=False
        )
    last_name = db.Column(
        db.String(MAX_LENGTH['last_name']),
        nullable=False
        )
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def __repr__(self):
        return "<User object email={0}>".format(self.email)
