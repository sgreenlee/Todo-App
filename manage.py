from flask.ext.script import Shell, Manager, Server
from application import create_app, db

app = create_app('development')
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db)
manager.add_command('shell', Shell(make_context=make_shell_context))

# development server configuration
server = Server(host='0.0.0.0', port=8000)
manager.add_command('runserver', server)

if __name__ == '__main__':
    manager.run()