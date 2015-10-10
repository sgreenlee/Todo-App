"""Configuration settings for Todo App"""

import os


class BaseConfiguration():
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')


class DevelopmentConfiguration(BaseConfiguration):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@localhost/{2}'.format(
        os.environ.get('DEV_DATABASE_ROLE'),
        os.environ.get('DEV_DATABASE_PW'),
        os.environ.get('DEV_DATABASE_NAME')
        )


class TestingConfiguration(BaseConfiguration):
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@localhost/{2}'.format(
        os.environ.get('TEST_DATABASE_ROLE'),
        os.environ.get('TEST_DATABASE_PW'),
        os.environ.get('TEST_DATABASE_NAME')
        )


class ProductionConfiguration(BaseConfiguration):
    SQLALCHEMY_DATABASE_URI = ''


configuration = {
    'development': DevelopmentConfiguration,
    'testing': TestingConfiguration,
    'production': ProductionConfiguration
    }
