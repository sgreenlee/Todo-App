from flask import render_template, redirect, url_for, flash, abort, request
from flask import jsonify, session
from flask.ext.login import current_user, login_required
from datetime import date
from . import main
from .forms import EditProfileForm, NewTaskForm, NewProjectForm
from ..models import db, User, Task, Project, Contribution, Goal, DAY_BITS
from ..email import send_confirmation_email
import random
import string
import json


def generate_csrf_token():
    """Return random string for CSRF token"""
    token = [random.choice(string.ascii_letters + string.digits)
             for _ in range(40)]
    return ''.join(token)


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
        return redirect(url_for('main.dashboard'))
    return render_template('add_task.html', form=form)


@main.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    """Get incomplete tasks for the current user and mark tasks as complete."""
    if request.method == 'GET':
        tasks = current_user.get_active_tasks()
        return render_template('tasks.html', tasks=tasks)
    elif request.method == 'POST':

        # check validity of csrf token
        if request.form.get('state') != session['state']:
            # print("\nInvalid state token")
            # print("Token from form:", request.form.get('state'))
            # print("Token from session:", session['state'])
            response = jsonify(failed='403 invalid csrf token')
            response.status_code = 403
            return response

        task_id = request.form.get('complete')
        task = Task.query.get(task_id)
        # if task does not belong to current user
        # raise 403 error
        if task.user != current_user.id:
            response = jsonify(failed='403 not authorized')
            response.status_code = 403
            return response
        task.completed_on = current_user.get_local_date()
        db.session.add(task)
        response = jsonify(success=task_id)
        response.status_code = 200
        return response


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


@main.route('/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    form = NewProjectForm()
    if form.validate_on_submit():
        # Create new project from form data
        new_project = Project(user=current_user.id, name=form.name.data,
                              description=form.description.data)
        db.session.add(new_project)
        db.session.commit()

        # Create goals from form data
        id = new_project.id
        goals = json.loads(request.form.get('goals'))
        for goal in goals:
            # skip invalid goals
            if goal['days'] == [] or int(goal['time']) == 0:
                continue
            days = sum([DAY_BITS[day] for day in goal['days']])
            time = int(goal['time'])
            db.session.add(Goal(project=id, days=days, time=time))
        db.session.commit()

        flash('Your new project has been created.')
        response = jsonify(redirect='/dashboard')
        response.status_code = 200
        return response


@main.route('/projects/contribute', methods=['POST'])
@login_required
def contribute_to_project():
    project_id = int(request.form.get('id'))
    project = Project.query.get(project_id)

    if project.user != current_user.id:
        response = jsonify(failed='403 Not authorized')
        response.status_code = 403
        return response

    time = int(request.form.get('time'))
    date = current_user.get_local_date()
    contribution = Contribution(project=project_id, time=time, date=date)
    db.session.add(contribution)
    db.session.commit()

    response = jsonify(status='success', id=project_id, time=time)
    response.status_code = 200
    return response


@main.route('/goals/delete', methods=['POST'])
@login_required
def delete_goal():
    """Delete a project goal."""

    # Check validity of csrf token
    if request.form.get('state') != session['state']:
        response = jsonify(failed='403 invalid csrf token')
        response.status_code = 403
        return response

    goal_id = request.form.get('id')
    goal = Goal.query.get(goal_id)

    # Check if goal belongs to current user
    if current_user.id != Project.query.get(goal.project).user:
        response = jsonify(failed='403 Not authorized')
        response.status_code = 403
        return response

    # Delete goal
    db.session.delete(goal)
    db.session.commit()

    flash("Your project goal has been deleted.")
    return redirect(url_for('main.dashboard'))


@main.route('/dashboard')
@login_required
def dashboard():
    """Show current user's tasks and projects."""

    # Generate a csrf token and
    # add to user session
    session['state'] = generate_csrf_token()

    # Get user's tasks
    tasks = current_user.get_active_tasks()

    # Projects
    today = date.today()
    goals = []
    project_goals = current_user.get_project_goals()
    for id, name, goal in project_goals:
        p = Project.query.get(id)
        contributed = p.time_contributed(start=current_user.get_local_date())
        goals.append((id, name, goal, contributed))

    projects = [project.to_dict() for project in current_user.projects]

    return render_template(
        'dashboard.html', tasks=tasks, goals=goals, projects=projects)


@main.route('/modals/projects')
@login_required
def all_projects():
    """Get information on all user's projects and goals."""
    projects = [project.to_dict() for project in current_user.projects]
    return render_template('modals/projects_modal.html', projects=projects)


@main.route('/modals/tasks/new', methods=['GET'])
@login_required
def new_task_modal():
    """Create a new task for the current user."""
    form = NewTaskForm()
    return render_template('modals/tasks_modal.html', form=form)


@main.route('/modals/projects/new', methods=['GET'])
@login_required
def new_project_modal():
    """Create a new project for the current user."""
    form = NewProjectForm()
    return render_template('modals/new_project_modal.html', form=form)
