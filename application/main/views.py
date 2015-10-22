from flask import render_template, redirect, url_for, flash
from flask.ext.login import current_user, login_required
from . import main
from .forms import EditProfileForm
from ..models import db, User
from ..email import send_confirmation_email


@main.route('/')
def index():
    """Home page."""
    return render_template('index.html')


@main.route('/profile')
@login_required
def view_profile():
    """Display user profile."""
    return(render_template('view_profile.html'))


@main.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile."""
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.email.data != current_user.email:
            # if user changes email, unconfirm user account
            # and send confirmation email to new address
            current_user.email = form.email.data
            current_user.is_confirmed = False
            send_confirmation_email(current_user)
            flash('A confirmation email has been sent to your new address.')
        # update user information
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('main.view_profile'))
    # load current user info for form defaults
    form.email.data = current_user.email
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    return render_template('edit_profile.html', form=form)
