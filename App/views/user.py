from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required
from flask_login import LoginManager
from.index import index_views

#from App.models import RegularUser, Todo
from functools import wraps

from App.controllers import (
    create_user,
    jwt_authenticate, 
    get_all_users,
    get_all_users_json,
    jwt_required,
    fetch_api_exercises,
    get_all_routines,
    get_user_routines,
    create_routine,
get_routine,
delete_routine,
update_routine
  
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')
#login_manager = LoginManager()


@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/exercises', methods=['GET'])
def display_exercises():
    exercises = fetch_api_exercises()
    print(exercises)
    print("exercises")
    return render_template('ExerciseList.html', exercises=exercises)

# @user_views.route('/routines', methods=['GET'])
# #@login_required
# def display_routnies():
#     routines = get_user_routines(current_user.id)
#     print(routines)
#     return render_template('ActualRoutinelist.html', users=routines)

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    create_user(data['username'], data['password'])
    return jsonify({'message': f"user {data['username']} created"})

@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')


# def user_required(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         if not current_user.is_authenticated or not isinstance(current_user, RegularUser):
#             return "Unauthorized", 401
#         return func(*args, **kwargs)
#     return wrapper
  
# @user_views.route('/app', methods=['GET'])
# @user_required
# def todos_page():
#   todos = todos = Todo.query.filter_by(user_id=current_user.id).all()
#   return render_template('todo.html', todos=todos)
@user_views.route('/routines', methods=['GET'])
@login_required
def display_routines():
    routines = get_user_routines(current_user.id)
    return render_template('ActualRoutinelist.html', routines=routines)

@user_views.route('/routine/create', methods=['GET', 'POST'])
@login_required
def create_routine2():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        user_id = current_user.id
        new_routine = create_routine(name=name, description=description, user_id=user_id)  # Update function name
        if new_routine:
            return redirect(url_for('user_views.display_routines'))  # Update endpoint name
    return render_template('routine_form.html', form_action=url_for('user_views.create_routine2'))  # Update endpoint name

@user_views.route('/routine/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_routine2(id):
    routine = get_routine(id)
    if not routine or routine.user_id != current_user.id:
        return redirect(url_for('user_views.display_routines'))

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        updated_routine = update_routine(id, name=name, description=description)
        if updated_routine:
            return redirect(url_for('user_views.display_routines'))

    return render_template('routine_form.html', form_action=url_for('user_views.edit_routine2', id=id), routine=routine)

@user_views.route('/routine/delete/<int:id>', methods=['POST'])
@login_required
def delete_routine(id):
    routine = get_routine(id)
    if not routine or routine.user_id != current_user.id:
        return redirect(url_for('user_views.display_routines'))

    deleted_routine = delete_routine(id)
    if deleted_routine:
        return redirect(url_for('user_views.display_routines'))

    return 'Failed to delete routine', 400

