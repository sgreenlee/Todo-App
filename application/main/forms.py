from flask.ext.wtf import Form
from wtforms import StringField, DateField, SubmitField, ValidationError
from wtforms.validators import Required, Email, Length
from ..models import MAX_LENGTH, User, Task


class EditProfileForm(Form):
    """Profile Edit Form."""
    # fields
    email = StringField('Email')
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    submit = SubmitField('Update Your Profile')
    # validators
    email.validators = [Required(), Length(1, MAX_LENGTH['email']), Email()]
    first_name.validators = [Length(1, MAX_LENGTH['first_name'])]
    last_name.validators = [Length(1, MAX_LENGTH['last_name'])]


class NewTaskForm(Form):
    """Form for creating a new task."""
    description = StringField('Description')
    description.validators = [Length(1, MAX_LENGTH['task_desc'])]
    deadline = DateField('Deadline')
    priority = StringField('Priority')
    priority.validators = [Length(1, MAX_LENGTH['task_priority'])]
    submit = SubmitField('Create Task')
