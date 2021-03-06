from flask_mail import Message
from threading import Thread
from flask import current_app, render_template
from . import mail


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(current_app.config['MAIL_SUBJECT_PREFIX'] + subject,
                  sender=current_app.config['MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def send_async_email(app, msg):
    """Send email asynchronously."""
    with app.app_context():
        mail.send(msg)


def send_confirmation_email(user):
    """Send account confirmation email to user."""
    token = user.generate_confirmation_token()
    send_email(user.email, 'Confirm your account', 'auth/email/confirm',
               token=token, user=user)


def send_password_reset_email(user):
    """Send password reset email to user."""
    token = user.generate_password_reset_token()
    send_email(user.email, 'Reset your password', 'auth/email/reset',
               token=token, user=user)
