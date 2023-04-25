from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user, LoginManager

from.index import index_views

from App.controllers import (
    create_user,
    jwt_authenticate,
    login ,
get_all_users,
get_all_users_json
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

'''
Page/Action Routes
'''





login_manager = LoginManager()

# def user_required(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         if not current_user.is_authenticated or not isinstance(current_user, RegularUser):
#             return "Unauthorized", 401
#         return func(*args, **kwargs)
#     return wrapper

# @login_manager.user_loader
# def load_user(user_id):
#   user =  RegularUser.query.get(user_id)
#   if user:
#     return user
#   return Admin.query.get(user_id)




  
  

@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@auth_views.route('/signup', methods=['GET'])
def get_user_page2():
    return render_template('signup.html')

@auth_views.route('/login', methods=['GET'])
def get_user_page3():
    return render_template('login.html')


@auth_views.route('/identify', methods=['GET'])
@login_required
def identify_page():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})


@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    user = login(data['username'], data['password'])
    if user:
        login_user(user)
        flash('Logged in successfully.')
        return redirect('/routines')
    return 'bad username or password given', 401

@auth_views.route('/logout', methods=['GET'])
def logout_action():
    logout_user()
    return '/'

'''
API Routes
'''

@auth_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@auth_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    create_user(data['username'], data['password'])
    
    return jsonify({'message': f"user {data['username']} created"})

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = jwt_authenticate(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  return jsonify(access_token=token)




@auth_views.route('/api/identify', methods=['GET'])
@login_required
def identify_user_action():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})