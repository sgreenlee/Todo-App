from application import create_app, db
from flask import current_app
import unittest


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        """Check that current_app exists."""
        self.assertFalse(current_app is None)

    def test_app_using_test_config(self):
        """Check that the testing configuration is being used."""
        self.assertTrue(current_app.config['TESTING'])
