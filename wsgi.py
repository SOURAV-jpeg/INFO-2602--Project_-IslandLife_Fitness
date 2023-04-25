import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import (create_user, get_all_users_json, get_all_users, login,create_routine)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.create_all()
  create_user('bob', 'bobpass')
  print('database intialized')


'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands')


# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
  create_user(username, password)
  print(f'{username} created!')


# this command will be : flask user create bob bobpass


@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
  if format == 'string':
    print(get_all_users())
  else:
    print(get_all_users_json())


app.cli.add_command(user_cli)  # add the group to the cli
'''
Test Commands
'''

test = AppGroup('test', help='Testing commands')


@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "UserUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
  else:
    sys.exit(pytest.main(["-k", "App"]))


@user_cli.command("login", help="Lists customers in the database")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def list_user_command2(username, password):
  res = login(username, password)
  if res:
    print(f'{username} logged in!')
  else:
    print('login unsuccessful!')


# @user_cli.command("addexercise", help="Adds an exercise to a routine")
# @click.argument("exercise_name")
# def add_exercise_command(exercise_name):
#     res = create_exercise(exercise_name)
#     if res:
#         print(f"{exercise_name} added")
#     else:
#         print("Failed to add exercise to routine")

@user_cli.command("addroutine", help="Adds a routine")
@click.argument("name")
@click.argument("description")
@click.argument("user_id")
def create_routine_command(name,description,user_id):
    res = create_routine(name, description, user_id)
    if res:
        print(f"{name} routine created")
    else:
        print("Failed to add routine")



app.cli.add_command(test)





# import click
# import csv
# #import tabulate
# #from models import db, RegularUser, Admin, Todo
# #from app import app
# from App.models import ( db, RegularUser,Admin,Todo )



# @app.cli.command("init2", help="Creates and initializes the database")
# def initialize2():
#   db.drop_all()
#   db.create_all()
#   pam = Admin('1123', 'pam', 'pam@mail.com', 'pampass')
#   bob = RegularUser('bob', 'bob@mail.com', 'bobpass')
#   rick = RegularUser('rick', 'rick@mail.com', 'rickpass')
#   sally = RegularUser('sally', 'sally@mail.com', 'sallypass')
#   users = [0, bob, rick, sally]
#   db.session.add_all([pam, bob, rick, sally]) #add all can save multiple objects at once
#   db.session.commit()
#   #load todo data from csv file
#   with open('todos.csv') as file:
#    reader = csv.DictReader(file)
#    for row in reader:
#      new_todo = Todo(text=row['text']) #create object
#      #update fields based on records
#      new_todo.done = True if row['done'] == 'true' else False
#      new_todo.user_id = users[int(row['user_id'])].id
#      db.session.add(new_todo) #queue changes for saving
#    db.session.commit() 
#    #save all changes OUTSIDE the loop
#   print('database intialized')




# @app.cli.command("create-user", help="Creates a user")
# @click.argument("username", default="rob")
# @click.argument("email", default="robmail")
# @click.argument("password", default="robpass")
# def create_user_command(username, email, password):
#   newuser = RegularUser(username, email, password)
#   try:
#     db.session.add(newuser)
#     db.session.commit()
#   except Exception as e:
#     db.session.rollback()
#     print(str(e))
#     print(f'{username} already exists!')
#   else:
#     print(f'{username} created!')


# @app.cli.command('get-users', help="Lists users in the app")
# def list_users_command():
#   users = RegularUser.query.all()
#   print(users)


# @app.cli.command('add-todo')
# @click.argument('username', default='bob')
# @click.argument('text', default='do work')
# def add_user_todo_command(username, text):
#   user = RegularUser.query.filter_by(username=username).first()
#   if user:
#     todo = user.add_todo(text)
#     print(f'todo:{todo.id} {text} created!')
#   else:
#     f'{username} not found!'


# @click.argument('username', default="bob")
# @app.cli.command('get-todos', help="Gets a user's todos")
# def get_user_todos_command(username):
#   user = RegularUser.query.filter_by(username=username).first()
#   if user:
#     print(user.todos)
#   else:
#     f'{username} not found!'


# @click.argument('todo_id', default=1)
# @click.argument('username', default='bob')
# @app.cli.command('toggle-todo')
# def toggle_todo_command(todo_id, username):
#   user = RegularUser.query.filter_by(username=username).first()
#   if not user:
#     print(f'{username} not found!')
#     return

#   todo = Todo.query.filter_by(id=todo_id, user_id=user.id).first()
#   if not todo:
#     print(f'{username} has no todo id {todo_id}')

#   todo.toggle()
#   print(f'{todo.text} is {"done" if todo.done else "not done"}!')

# @click.argument('username', default='bob')
# @click.argument('todo_id', default=6)
# @click.argument('category', default='chores')
# @app.cli.command('add-category', help="Adds a category to a todo")
# def add_todo_category_command(username, todo_id, category):
#   user = RegularUser.query.filter_by(username=username).first()
#   if not user:
#     print(f'{username} not found!')
#     return

#   res = user.add_todo_category(todo_id, category)
#   if not res:
#     print(f'{username} has no todo id {todo_id}')
#     return

#   print('Category added!')

# # @app.cli.command('list-todos')
# # def list_todos():
# #   #tabulate package needs to work with an array of arrays
# #   data = []
# #   for todo in Todo.query.all():
# #     data.append([ todo.text, todo.done, todo.user.username, todo.cat_list()])
# #   print (tabulate(data, headers=["Text", "Done", "User", "Categories"]))







