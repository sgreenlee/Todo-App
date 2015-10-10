from flask import Flask
from models import db
from config import configuration


def create_app(config_name='development'):
    """Create a flask application object with the specified configuration
        settings."""

    app = Flask(__name__)
    app.config.from_object(configuration[config_name])

    db.init_app(app)

    # attach routes here

    return app
