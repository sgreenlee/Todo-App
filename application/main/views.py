from flask import render_template, redirect, url_for, flash, abort, request
from flask.ext.login import current_user, login_required
from datetime import date
from . import main
from .forms import EditProfileForm, NewTaskForm
from ..models import db, User, Task
from ..email import send_confirmation_email


@main.route('/')
def index():
    """Home page."""
    return render_template('index.html')


@main.route('/profile')
@login_required
def view_profile():
    """Display user profile."""
    return(render_template('view_profile.html'))


@main.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile."""
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.email.data != current_user.email:
            # if user changes email, unconfirm user account
            # and send confirmation email to new address
            current_user.email = form.email.data
            current_user.is_confirmed = False
            send_confirmation_email(current_user)
            flash('A confirmation email has been sent to your new address.')
        # update user information
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('main.view_profile'))
    # load current user info for form defaults
    form.email.data = current_user.email
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    return render_template('edit_profile.html', form=form)


@main.route('/tasks/add', methods=['GET', 'POST'])
@login_required
def add_task():
    """Create a new task for the current user."""
    form = NewTaskForm()
    if form.validate_on_submit():
        new_task = Task(
            user=current_user.id,
            description=form.description.data,
            deadline=form.deadline.data,
            priority=form.priority.data)
        db.session.add(new_task)
        db.session.commit()
        flash("Your new task has been created.")
        return redirect(url_for('main.tasks'))
    return render_template('add_task.html', form=form)


@main.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    """Get incomplete tasks for the current user and mark tasks as complete."""
    if request.method == 'GET':
        tasks = current_user.get_active_tasks()
        return render_template('get_tasks.html', tasks=tasks)
    elif request.method == 'POST':
        try:
            task_id = request.form.get('complete')
            task = Task.query.get(task_id)
            # if task does not belong to current user
            # raise 403 error
            if task.user != current_user.id:
                abort(403)
            task.completed_on = date.today()
            db.session.add(task)
            flash("This task has been marked as complete.")
            return redirect(url_for('main.tasks'))
        except:
            # bad request
            abort(400)


@main.route('/projects', methods=['GET'])
@login_required
def projects():
    """View and add time to projects with active goals for today."""
    # if url contains query string with 'id' and 'time' params
    # create a contribution to the project corresponding to 'id'
    if request.args.get('id') and request.args.get('time'):
        project_id = request.args.get('id')
        time = int(request.args.get('time'))
        contribution = Contribution(project=project_id, time=time)
        db.session.add(contribution)
        db.session.commit()
    today = date.today()
    todays_projects = []
    projects = current_user.get_projects()
    # loop through user's projects if a project has active goals then append
    # a tuple with the project's name, the time goal for today, and the
    # amount of time contributed today to todays_projects
    for project in projects:
        goal = project.time_goal()
        if goal:
            todays_projects.append(
                (project.id, project.name, goal,
                 project.time_contributed(start=today)))
    return render_template('projects.html', projects=todays_projects)


@main.route('/dashboard')
@login_required
def dashboard():
    """Show current user's tasks and projects."""
    #  Tasks
    tasks = current_user.get_active_tasks()

    #  Projects
    today = date.today()
    todays_projects = []
    projects = current_user.get_projects()
    # loop through user's projects if a project has active goals then append
    # a tuple with the project's name, the time goal for today, and the
    # amount of time contributed today to todays_projects
    for project in projects:
        goal = project.time_goal()
        if goal:
            todays_projects.append(
                (project.id, project.name, goal,
                 project.time_contributed(start=today)))
    return render_template(
        'dashboard.html', tasks=tasks, projects=todays_projects)
