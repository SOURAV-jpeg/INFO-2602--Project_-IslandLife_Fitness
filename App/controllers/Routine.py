from App.models import Routine, Exercise
from App.database import db

def create_routine(name, description, user_id):
    new_routine = Routine(name=name, description=description, user_id=user_id)
    db.session.add(new_routine)
    db.session.commit()
    return new_routine

def get_routine(id):
    return Routine.query.get(id)

def get_all_routines():
    return Routine.query.all()

def get_user_routines(user_id):
    return Routine.query.filter_by(user_id=user_id).all()

def update_routine(id, name=None, description=None):
    routine = get_routine(id)
    if routine:
        if name:
            routine.name = name
        if description:
            routine.description = description
        db.session.add(routine)
        db.session.commit()
        return routine
    return None

def delete_routine(id):
    routine = get_routine(id)
    if routine:
        db.session.delete(routine)
        db.session.commit()
        return routine
    return None

def add_exercise_to_routine(routine_id, exercise_id):
    routine = get_routine(routine_id)
    exercise = Exercise.query.get(exercise_id)
    if routine and exercise:
        routine.add_exercise(exercise)
        return routine
    return None

def remove_exercise_from_routine(routine_id, exercise_id):
    routine = get_routine(routine_id)
    exercise = Exercise.query.get(exercise_id)
    if routine and exercise:
        routine.remove_exercise(exercise)
        return routine
    return None
