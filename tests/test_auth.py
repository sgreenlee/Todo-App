import unittest
from flask import url_for
import re
from application import create_app, db
from application.models import User


class TestAuth(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_and_login(self):
        """Test registering and logging in a new user."""
        # register new account
        response = self.client.post(
            url_for('auth.register'),
            data={
                'email': 'sam.a.greenlee@gmail.com',
                'first_name': 'Sam',
                'last_name': 'Greenlee',
                'password': 'llama',
                'password2': 'llama'
                },
            follow_redirects=True)
        self.assertTrue(
            response.status_code == 200,
            'HTTP Response status code is: {0}'.format(response.status_code))
        data = response.get_data(as_text=True)
        self.assertTrue(
            'You have successfully registered' in data,
            "'You have successfully registered' does not appear in response")

        # find new account in database
        user = User.query.filter_by(email='sam.a.greenlee@gmail.com').first()
        self.assertIsNotNone(user, 'New user not found in database')
        self.assertEqual(
            user.first_name, 'Sam',
            'New user has incorrect first name: {0}'.format(user.first_name))
        self.assertEqual(
            user.last_name, 'Greenlee',
            'New user has incorrect last name: {0}'.format(user.last_name))
        self.assertFalse(user.is_confirmed, 'New user is confirmed')

        # log in with new account
        response = self.client.post(
            url_for('auth.login'),
            data={
                'email': 'sam.a.greenlee@gmail.com',
                'password': 'llama'
                },
            follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue(
            re.search('Welcome,\s+Sam', data),
            "Home page displays user's name after login.")

        # confirm new user
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('auth.confirm', token=token),
                                   follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('Thank you for confirming your account!' in data)
        self.assertTrue(user.is_confirmed, "user is now confirmed")

        # log out user
        response = self.client.get(url_for('auth.logout'),
                                   follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('You have been logged out.' in data)
