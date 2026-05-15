from ..extensions import db

class WorkoutPlan(db.Model):
    __tablename__ = 'workout_plans'
    plan_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.trainer_id'), nullable=False)

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    exercises = db.relationship('WorkoutExercise', backref='workout_plan', lazy=True, cascade='all, delete-orphan')
    sessions = db.relationship('WorkoutSession', backref='plan', lazy=True)