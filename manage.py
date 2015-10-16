from flask.ext.script import Shell, Manager, Server
from application import create_app, db
from application.models import User

app = create_app('development')
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, User=User)
manager.add_command('shell', Shell(make_context=make_shell_context))

# development server configuration
server = Server(host='0.0.0.0', port=8000)
manager.add_command('runserver', server)

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()