from flask import render_template, redirect, request, url_for, flash
from flask import current_app
from flask.ext.login import login_user, logout_user, login_required
from flask.ext.login import current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_confirmation_email, send_password_reset_email
from .forms import LoginForm, RegistrationForm, RequestPasswordResetForm
from .forms import ResetPasswordForm
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Log in user."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """Log out current user."""
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            email=form.email.data,
            password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        send_confirmation_email(new_user, token)
        flash("You have successfully registered. A confirmation email has"
              "been sent to you at {0}.".format(new_user.email))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    """Confirm user account corresponding to token."""
    if current_user.is_confirmed:
        return(redirect(url_for('main.index')))
    if current_user.confirm(token):
        flash("Thank you for confirming your account!")
    else:
        flash("The confirmation link is invalid or expired.")
    return(redirect(url_for('main.index')))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    """Resend confirmation email to currently authenticated user."""
    if current_user.is_confirmed:
        return(redirect(url_for('main.index')))
    send_confirmation_email(current_user)
    flash("A new confirmation message has been sent. Please check your email.")
    return(redirect(url_for('main.index')))


@auth.route('/reset', methods=['GET', 'POST'])
def request_password_reset():
    """Request password reset email."""
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_password_reset_email(user)
        flash('A password reset link has been sent to you by email.')
        return(redirect(url_for('auth.login')))
    return(render_template('auth/request_password_reset.html', form=form))


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset user password."""
    s = Serializer(current_app.config['SECRET_KEY'])
    data = s.loads(token)
    user_id = data.get('reset')
    user = User.query.get(int(user_id))
    if user is None:
        flash('The password reset link is invalid or expired.')
        return(redirect(url_for('main.index')))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        flash('You have successfully changed your password.')
        return(redirect(url_for('auth.login')))
    return(render_template('auth/reset_password.html', form=form))
