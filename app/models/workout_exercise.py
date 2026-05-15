from ..extensions import db

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    workout_plan_id = db.Column(db.Integer, db.ForeignKey('workout_plans.plan_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    sets = db.Column(db.Integer, default=3)
    reps = db.Column(db.Integer, default=10)
    rest_seconds = db.Column(db.Integer, default=60)
    notes = db.Column(db.String(200))
    
    # No explicit relationship here; it's provided by the backref in WorkoutPlan.exercises