from App.database import db

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    muscles = db.Column(db.String(100), nullable=False)
    equipment = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    instructions = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    
    
    difficulty = db.Column(db.Integer, nullable=False)

    def __init__(self, name, type, description, equipment, muscles, difficulty, instructions):
        self.name = name
        self.type = type
        self.description = description
        self.equipment = equipment
        self.muscles = muscles
        self.difficulty = difficulty
        self.instructions = instructions

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'equipment': self.equipment,
            'muscles': self.muscles,
            'difficulty': self.difficulty
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
