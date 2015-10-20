"""Configuration settings for Todo App"""

import os


class BaseConfiguration():
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SUBJECT_PREFIX = '[Protaskinate] '
    MAIL_SENDER = 'Protaskinate Admin <protaskinate@fakeemail.com>'


class DevelopmentConfiguration(BaseConfiguration):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@localhost/{2}'.format(
        os.environ.get('DEV_DATABASE_ROLE'),
        os.environ.get('DEV_DATABASE_PW'),
        os.environ.get('DEV_DATABASE_NAME')
        )
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('DEV_MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('DEV_MAIL_PASSWORD')


class TestingConfiguration(BaseConfiguration):
    TESTING = True
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
