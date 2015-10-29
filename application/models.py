from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime
import pytz
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
    'last_name': 20,
    'task_desc': 128,
    'task_priority': 12,
    'project_name': 20,
    'project_desc': 128
}

DAYS = {
    'MON': 0b0000001,
    'TUE': 0b0000010,
    'WED': 0b0000100,
    'THU': 0b0000100,
    'FRI': 0b0001000,
    'SAT': 0b0010000,
    'SUN': 0b0100000
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
    timezone = db.Column(db.String(30), default='UTC')
    password_hash = db.Column(db.String(128), nullable=False)
    is_confirmed = db.Column(db.Boolean, default=False)
    tasks = db.relationship('Task', backref='users')

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

    def get_active_tasks(self):
        """Return all incomplete tasks for this user."""
        qry = Task.query.filter_by(user=self.id)
        qry = qry.filter_by(completed_on=None)
        return qry.all()

    def get_local_date(self):
        """Returns date object for user's current local date."""
        tz = pytz.timezone(self.timezone)
        utc = pytz.utc
        utc_now = datetime.datetime.now(utc)
        return utc_now.astimezone(tz).date()

    def __repr__(self):
        return "<User object: {0}>".format(self.email)


class Task(db.Model):
    """Represents non-recurring tasks that are either complete or
    incomplete."""

    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(MAX_LENGTH['task_desc']), nullable=False)
    deadline = db.Column(db.Date, default=None)
    completed_on = db.Column(db.Date, default=None)
    priority = db.Column(db.String(MAX_LENGTH['task_priority']), default=None)

    def __repr__(self):
        return "<Task object: {0}>".format(self.description)


class Project(db.Model):
    """Represents long-running projects with defined time goals."""

    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(MAX_LENGTH['project_name']), nullable=False)
    description = db.Column(db.String(MAX_LENGTH['project_desc']))

    def time_contributed(self, start=None, end=None):
        """Return amount of time contributed to a project between optional
        date limits start and end."""

        sum = 0
        qry = Contribution.query.filter_by(project=self.id)

        # apply date filters
        if start:
            qry = qry.filter(Contribution.date >= start)
        if end:
            qry = qry.filter(Contribution.date <= end)

        contributions = qry.all()
        for contribution in contributions:
            sum += contribution.time
        return sum

    def time_goal(self, date=None):
        """Return user goal for amount of time contributed to this project
        on date. If no date supplied, return goal for today."""

        target_date = date or datetime.date.today()
        sum = 0

        goals = Goal.query.filter_by(project=self.id).all()
        for goal in goals:
            # check if goal applies to target date
            if (2 ** target_date.weekday() & goal.days):
                sum += goal.time
        return sum


class Contribution(db.Model):
    """Represents a discrete amount of time (in minutes) contributed to a
    project."""

    __tablename__ = 'contributions'

    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.Integer, db.ForeignKey('projects.id'),
                        nullable=False)
    time = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date)
    __table_args__ = (
        db.CheckConstraint(time > 0, name='time is positive'),
        )

    def __init__(self, project, time, date=datetime.date.today()):
        self.project = project
        self.time = time
        self.date = date


class Goal(db.Model):
    """Represents a time-commitment goal for a project."""

    __tablename__ = 'goals'

    id = db.Column(db.Integer(), primary_key=True)
    project = db.Column(db.Integer(), db.ForeignKey('projects.id'),
                        nullable=False)
    days = db.Column(db.Integer(), nullable=False)
    time = db.Column(db.Integer(), nullable=False)
    __table_args__ = (
        db.CheckConstraint(time > 0, name='time is positive'),
        )
