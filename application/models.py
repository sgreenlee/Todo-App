from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask.ext.login import UserMixin
from flask.ext.login import LoginManager
from flask import current_app

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
        nullable=True
        )
    last_name = db.Column(
        db.String(MAX_LENGTH['last_name']),
        nullable=True
        )
    password_hash = db.Column(db.String(128), nullable=False)
    is_confirmed = db.Column(db.Boolean, default=False)

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

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') is None:
            return False
        if data.get('confirm') == self.id:
            self.is_confirmed = True
            db.session.add(self)
            return True
        else:
            return False

    def generate_password_reset_token(self, expiration=3600):
        """Return password reset token."""
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def __repr__(self):
        return "<User object email={0}>".format(self.email)
