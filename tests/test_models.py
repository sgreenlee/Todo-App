import unittest
from flask import current_app
from application import create_app, db
from application.models import User


class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @staticmethod
    def create_steve():
        """Create a generic user for testing"""
        steve = User(
            email='steve@steve.com',
            first_name='Steve',
            last_name='Stephens'
            )
        return steve

    def test_password_set_only(self):
        """Trying to read the User password property raises an exception"""
        steve = TestModels.create_steve()
        with self.assertRaises(AttributeError):
            steve.password

    def test_password_hash(self):
        """Check that password hashing and verifying is working"""
        steve = TestModels.create_steve()
        steve.password = 'aardvark'
        self.assertTrue(steve.password_hash is not None)
        self.assertTrue(steve.verify_password('aardvark'))
