from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, ValidationError
from wtforms.fields.html5 import DateField
from wtforms.validators import Required, Email, Length, Optional
from ..models import MAX_LENGTH, User, Task


class EditProfileForm(Form):
    """Profile Edit Form."""
    # fields
    email = StringField(
        'Email',
        validators=[Required(), Length(1, MAX_LENGTH['email']), Email()])
    first_name = StringField(
        'First Name',
        validators=[Length(0, MAX_LENGTH['first_name'])])
    last_name = StringField(
        'Last Name',
        validators=[Length(0, MAX_LENGTH['last_name'])])
    submit = SubmitField('Update Your Profile')


class NewTaskForm(Form):
    """Form for creating a new task."""
    description = StringField(
        'Description',
        validators=[Required(), Length(1, MAX_LENGTH['task_desc'])])
    deadline = DateField('Deadline', validators=[Optional()])
    priority = StringField(
        'Priority', validators=[Length(0, MAX_LENGTH['task_priority'])])
    submit = SubmitField('Create Task')


class NewProjectForm(Form):
    """Form for creating a new project."""
    name = StringField('Name', validators=[Required()])
    description = StringField('Description')
    submit = SubmitField('Create Project')
