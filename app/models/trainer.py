from ..extensions import db

class Trainer(db.Model):
    __tablename__ = 'trainers'
    trainer_id = db.Column (db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    specialization = db.Column(db.String(100))
    bio = db.Column(db.Text)
    hourly_rate = db.Column(db.Numeric(10, 2))
    certifications = db.Column(db.Text)

    clients = db.relationship('Client', backref='trainer', lazy=True)
    workout_plans = db.relationship('WorkoutPlan', backref='trainer', lazy=True)
    session_booking = db.relationship('SessionBooking', backref='trainer', laayzy=True)

