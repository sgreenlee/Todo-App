from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import HiddenField, ValidationError
from wtforms.validators import Required, Email, Length, EqualTo
from ..models import MAX_LENGTH, User


class LoginForm(Form):
    email = StringField(
        'Email',
        validators=[Required(), Length(1, MAX_LENGTH['email']), Email()]
        )
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    email = StringField('Email', validators=[Required(),
                                             Length(1, MAX_LENGTH['email']),
                                             Email()])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm Password', validators=[Required()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class RequestPasswordResetForm(Form):
    email = StringField('Email')
    email.validators = [Required(), Length(1, MAX_LENGTH['email']), Email()]
    submit = SubmitField('Send Email')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Invalid Email Address')


class ResetPasswordForm(Form):
    password = PasswordField('New Password')
    password.validators = [
        Required(),
        EqualTo('password2', message='Passwords must match.')]
    password2 = PasswordField('Confirm New Password', validators=[Required()])
    submit = SubmitField('Reset Password')
