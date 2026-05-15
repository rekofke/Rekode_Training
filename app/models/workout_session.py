from ..extensions import db

class WorkoutSession(db.Model):
    __tablename__ = 'workout_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.trainer_id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('workout_plans.plan_id'), nullable=True)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    capacity = db.Column(db.Integer, default=15)
    booked_count = db.Column(db.Integer, default=0)
    
    # Relationships
    trainer = db.relationship('Trainer', backref='workout_sessions')
    bookings = db.relationship('SessionBooking', backref='workout_session', lazy=True)