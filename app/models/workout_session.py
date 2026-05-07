from ..extensions import db

class WorkoutSession(db.Model):
    __tablename_ = 'Workout_sessions'
    session_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, ForeignKey=True)
    plan_id = db.Column(db.Integer, ForeignKey=True)
    dae = db.Column(db.Date, server_default=db.func.now())
    completed = db.Column(db.Boolean, default=True)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)