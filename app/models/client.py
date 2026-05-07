from ..extensions import db

class Client(db.Model):
    __tablename__ = 'clients'
    client_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    fitness_goals = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.trainer_id'))

    workout_plans = db.relationship('WorkoutPlan', backref='client', lazy=True)
    workout_sessions = db.relationship('WorkoutSession', backref='client', lazy=True)
    session_bookings = db.relationship('SessionBooking', backref='client', lazy=True)
    progress_logs = db.relationship('ProgressLog', backref='client', lazy=True)
