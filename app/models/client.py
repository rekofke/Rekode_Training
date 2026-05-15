from ..extensions import db

class Client(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.trainer_id'))
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    membership_type = db.Column(db.String(50))
    
    # Relationships
    user = db.relationship('User', backref='client_profile')
    progress_logs = db.relationship('ProgressLog', backref='client')
    
    # DO NOT add: workout_sessions = db.relationship('WorkoutSession')