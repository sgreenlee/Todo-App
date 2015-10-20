from flask import Flask
from models import db, login_manager
from config import configuration
from flask_bootstrap import Bootstrap
from flask_mail import Mail

mail = Mail()


def create_app(config_name='development'):
    """Create a flask application object with the specified configuration
        settings."""

    app = Flask(__name__)
    app.config.from_object(configuration[config_name])

    Bootstrap(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # register blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
