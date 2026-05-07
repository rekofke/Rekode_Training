from ..extensions import db

class WorkoutExercise(db.Model):
    __table__ = 'workout_exercise'
    exercise_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('workout_plans.plan_id'), nullable=False)
    exercise_name = db.Column(db.String(100), nullable=False)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weight = db.Column(db.String(20)) # e.g. "50 kg" or "bodyweight"
    notes = db.Column(db.StringO(200))
    
     
