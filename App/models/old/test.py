import uuid
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql.expression import func
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


def generate_short_uuid():
  return str(uuid.uuid4())[:8]


class User2(db.Model, UserMixin):
  __abstract__ = True
  id = db.Column(db.String(8),
                 primary_key=True,
                 default=generate_short_uuid,
                 server_default='gen_random_uuid()')
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)

  def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.set_password(password)

  def get_json(self):
    return {
      "id": self.id,
      "username": self.username,
      "email": self.email,
      "password": self.password
    }

  def set_password(self, password):
    """Create hashed password."""
    self.password = generate_password_hash(password, method='sha256')

  def check_password(self, password):
    """Check hashed password."""
    return check_password_hash(self.password, password)

  def __repr__(self):
    return f'<User {self.username} - {self.email}>'


class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer,
                      db.ForeignKey('regular_user.id'),
                      nullable=False)  #set userid as a foreign key to user.id
  text = db.Column(db.String(255), nullable=False)
  done = db.Column(db.Boolean, default=False)

  def __init__(self, text):
    self.text = text

  def toggle(self):
    self.done = not self.done
    db.session.add(self)
    db.session.commit()

  def cat_list(self):
    return ', '.join([category.text for category in self.categories])

  def get_json(self):
    return {
      "id": self.id,
      "text": self.text,
      "done": self.done,
      "categories": self.cat_list()
    }

  def __repr__(self):
    return f'<Todo: {self.id} | {self.user.username} | {self.text} | { "done" if self.done else "not done" } | categories {self.cat_list()}>'


class TodoCategory(db.Model):
  __tablename__ = 'todo_category'
  id = db.Column(db.Integer, primary_key=True)
  todo_id = db.Column(db.Integer, db.ForeignKey('todo.id'), nullable=False)
  category_id = db.Column(db.Integer,
                          db.ForeignKey('category.id'),
                          nullable=False)
  last_modified = db.Column(db.DateTime,
                            default=func.now(),
                            onupdate=func.now())

  def __repr__(self):
    return f'<TodoCategory last modified {self.last_modified.strftime("%Y/%m/%d, %H:%M:%S")}>'


class Category(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer,
                      db.ForeignKey('regular_user.id'),
                      nullable=False)
  text = db.Column(db.String(255), nullable=False)
  user = db.relationship('RegularUser',
                         backref=db.backref('categories', lazy='joined'))
  todos = db.relationship('Todo',
                          secondary='todo_category',
                          backref=db.backref('categories', lazy=True))

  def __init__(self, user_id, text):
    self.user_id = user_id
    self.text = text

  def __repr__(self):
    return f'<Category user:{self.user2.username} - {self.text}>'

  def get_json(self):
    return {
      "id": self.id,
      "user_id": self.user_id,
      "user": self.user.username,
      "text": self.text
    }


class RegularUser(User2):
  __tablename__ = 'regular_user'
  todos = db.relationship(
    'Todo', backref='user2',
    lazy=True)  # sets up a relationship to todos which references User

  def add_todo(self, text):
    new_todo = Todo(text=text)
    new_todo.user_id = self.id
    self.todos.append(new_todo)
    db.session.add(self)
    db.session.commit()
    return new_todo

  def delete_todo(self, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=self.id).first()
    if todo:
      db.session.delete(todo)
      db.session.commit()
      return True
    return None

  def update_todo(self, todo_id, text):
    todo = Todo.query.filter_by(id=todo_id, user_id=self.id).first()
    if todo:
      todo.text = text
      db.session.add(todo)
      db.session.commit()
      return todo
    return None

  def toggle_todo(self, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=self.id).first()
    if todo:
      todo.toggle()
      return Todo
    return None

  def add_todo_category(self, todo_id, category_text):
    category = Category.query.filter_by(text=category_text).first()
    todo = Todo.query.filter_by(id=todo_id, user_id=self.id).first()

    # todo_id given does not exist or belong to user
    if not todo:
      return None

    # create category if it doesn't exist
    if not category:
      category = Category(self.id, category_text)
      db.session.add(category)
      db.session.commit()

    #check if todo already has the category
    if category not in todo.categories:
      category.todos.append(todo)
      db.session.add(category)
      db.session.commit()
    return category

  def getNumTodos(self):
    return len(self.todos)

  def getDoneTodos(self):
    numDone = 0
    for todo in self.todos:
      if todo.done:
        numDone += 1
    return numDone

  def get_json(self):
    return {
      "id": self.id,
      "username": self.username,
      "email": self.email,
      "role": 'regular user'
    }

  def __repr__(self):
    return f'<RegularUser {self.id} : {self.username} - {self.email}>'


class Admin(User2):
  __tablename__ = 'admin'
  staff_id = db.Column(db.String(120), unique=True, nullable=False)

  def get_all_todos_json(self):
    todos = Todo.query.all()
    if todos:
      return [todo.get_json() for todo in todos]
    else:
      return []

  def get_all_todos(self):
    return Todo.query.all()

  def get_done_stats(self):
    todos = Todo.query.all()
    res = {}
    for todo in todos:
      if todo.done:
        if todo.user.username in res:
          res[todo.user.username]+=1
        else:
          res[todo.user.username]=1
    return res

  def get_todo_stats(self):
    todos = Todo.query.all()
    res = {}
    for todo in todos:
      if todo.user.username in res:
        res[todo.user.username]+=1
      else:
        res[todo.user.username]=1
    return res

  def search_todos(self, q, done, page): 
      matching_todos = None
    
      if q!="" and done=="any" :
        #search query and done is any - just do search
        matching_todos = Todo.query.join(RegularUser).filter(
          db.or_(RegularUser.username.ilike(f'%{q}%'), Todo.text.ilike(f'%{q}%'), Todo.id.ilike(f'%{q}%'))
        )
      elif q!="":
        #search query and done is true or false - search then filter by done
        is_done = True if done=="true" else False
        matching_todos = Todo.query.join(RegularUser).filter(
          db.or_(RegularUser.username.ilike(f'%{q}%'), Todo.text.ilike(f'%{q}%'), Todo.id.ilike(f'%{q}%')),
          Todo.done == is_done
        )
      elif done != "any":
        # done is true/false but no search query - filter by done only
        is_done = True if done=="true" else False
        matching_todos = Todo.query.filter_by(
            done= is_done
        )
      else:
        # done is any and no search query - all results
        matching_todos = Todo.query
        
      return matching_todos.paginate(page=page, per_page=10)

  def __init__(self, staff_id, username, email, password):
    super().__init__(username, email, password)
    self.staff_id = staff_id

  def get_json(self):
    return {
      "id": self.id,
      "username": self.username,
      "email": self.email,
      "role": 'admin'
    }

  def __repr__(self):
    return f'<Admin {self.id} : {self.username} - {self.email}>'
