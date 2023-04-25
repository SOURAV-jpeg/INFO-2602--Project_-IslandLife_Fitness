from App.database import db

exercise_routine = db.Table('exercise_routine',
    db.Column('exercise_id', db.Integer, db.ForeignKey('exercise.id'), primary_key=True),
    db.Column('routine_id', db.Integer, db.ForeignKey('routine.id'), primary_key=True)
)

class Routine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('routines', lazy=True))
    exercises = db.relationship('Exercise', secondary=exercise_routine, backref=db.backref('routines', lazy=True))

    def __init__(self, name, description, user_id):
        self.name = name
        self.description = description
        self.user_id = user_id

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id,
            'exercises': [exercise.to_dict() for exercise in self.exercises]
        }

    def add_exercise(self, exercise):
        if exercise not in self.exercises:
            self.exercises.append(exercise)
            db.session.commit()

    def remove_exercise(self, exercise):
        if exercise in self.exercises:
            self.exercises.remove(exercise)
            db.session.commit()
