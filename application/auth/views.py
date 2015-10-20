from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required
from flask.ext.login import current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm


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
        token = new_user.generate_confirmation_token()
        send_email(new_user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=new_user, token=token)
        flash("You have successfully registered. A confirmation email has"
              "been sent to you at {0}.".format(new_user.email))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
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
    if current_user.is_confirmed:
        return(redirect(url_for('main.index')))
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user,
               token=token)
    flash("A new confirmation message has been sent. Please check your email.")
    return(redirect(url_for('main.index')))
