from flask import Flask
from models import db
from config import configuration
from flask_bootstrap import Bootstrap
from flask.ext.login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name='development'):
    """Create a flask application object with the specified configuration
        settings."""

    app = Flask(__name__)
    app.config.from_object(configuration[config_name])

    Bootstrap(app)
    db.init_app(app)
    login_manager.init_app(app)

    # attach routes here

    return app
