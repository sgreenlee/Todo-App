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

    def test_password_setter(self):
        """Setting user password creates password_hash attribute"""
        steve = TestModels.create_steve()
        steve.password = 'cat'
        self.assertTrue(steve.password_hash is not None)

    def test_password_hash(self):
        """Test password hashing and verifying"""
        steve = TestModels.create_steve()
        steve.password = 'aardvark'
        self.assertTrue(steve.verify_password('aardvark'))
        self.assertFalse(steve.verify_password('llama'))
