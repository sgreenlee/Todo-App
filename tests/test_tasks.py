import unittest
from flask import url_for
from application import create_app, db
from application.models import User, Task


class TestTasks(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)
        db.create_all()
        # create test user
        user = User(
            email='alansmith@fakeemail.com',
            first_name='Alan',
            last_name='Smith',
            password='llama'
            )
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_tasks(self):
        """Test creating a new task, getting active tasks
        and marking tasks complete."""
        # log in with test user
        response = self.client.post(url_for('auth.login'), data={
                'email': 'alansmith@fakeemail.com',
                'password': 'llama'},
            follow_redirects=True)
        data = response.get_data(as_text=True)

        # test login succeeds
        err_msg = 'Login unsuccessful'
        self.assertTrue('Welcome, Alan' in data, err_msg)

        # create new task
        response = self.client.post(url_for('main.add_task'), data={
                'description': 'do the laundry',
                'deadline': '2034-10-01',
                'priority': 'LOW'
            })
        err_msg = 'New task creation unsuccessful: http response status is {0}'
        self.assertTrue(response.status_code == 201,
                        err_msg.format(response.status_code))

        # get active tasks
        response = self.client.get(url_for('main.get_tasks'))
        data = response.get_data(as_text=True)
        err_msg = 'Get tasks failed: "do the laundry" not in response'
        self.assertTrue('do the laundry' in data)

        # create another task
        response = self.client.post(url_for('main.add_task'), data={
                'description': 'pay parking ticket',
                'deadline': '2034-05-01',
                'priority': 'HIGH'
            })
        err_msg = 'Second task not created: http response status is {0}'
        self.assertTrue(response.status_code == 201,
                        err_msg.format(response.status_code))

        # get new tasks
        response = self.client.get(url_for('main.get_tasks'))
        data = response.get_data(as_text=True)
        err_msg = 'Get tasks failed: could not find both tasks'
        self.assertTrue(
            'do the laundry' in data and 'pay parking ticket' in data, err_msg)

        # mark a task as complete
        task = Task.query.filter_by(description='pay parking ticket').first()
        response = self.client.post(url_for('main.complete_task'), data={
                'id': task.id
            })
        err_msg = 'Complete task failed: completed_on is None'
        self.assertTrue(task.completed_on is not None, err_msg)

        # get tasks again
        response = self.client.get(url_for('main.get_tasks'))
        data = response.get_data(as_text=True)

        err_msg = 'Get tasks failed: incomplete task not in data'
        self.assertTrue('do the laundry' in data, err_msg)

        # test that completed task does not appear in response
        err_msg = 'Get tasks failed: completed task in data'
        self.assertTrue('pay parking ticket' not in data)
