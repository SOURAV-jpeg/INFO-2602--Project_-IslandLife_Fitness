from App.models import User
#from App.models import Routine
from App.database import db
import requests
import os


def create_user(username, password):
    newuser = User(username=username, password=password)
    try:
        db.session.add(newuser)
        db.session.commit()
        return newuser
    except:
        return None

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None


def fetch_api_exercises():
  key = 'EXERCISE_API_KEY'

  url = "https://api.api-ninjas.com/v1/exercises"
  headers = {
      "X-Api-Key": os.getenv(key)
  }
  params = {
      "muscle": "calves",
      "offset": 0,
      "limit": 10
  }
  
  response = requests.get(url, headers=headers, params=params)
  
  if response.status_code == 200:
      exercises = response.json()
      for exercise in exercises:
          print(f"Name: {exercise['name']}")
          print(f"Type: {exercise['type']}")
          print(f"Muscle: {exercise['muscle']}")
          print(f"Equipment: {exercise['equipment']}")
          print(f"Difficulty: {exercise['difficulty']}")
          print(f"Instructions: {exercise['instructions']}")
          print("\n")
  else:
      print(f"Error: {response.status_code}")
    
  if response.status_code == 200:
      exercises = response.json()
      #exercises = [1,2,3,4,5]
      return exercises
  else:
      return(f"Error: {response.status_code}")