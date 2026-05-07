from ..extensions import db

class SessionBooking(db.Model):
    __tablename__ = 'session_bookings'
    booking_id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.trainer_id'), nullable=False)
    client_id = db.Column(db.Integer('clients.client_id'), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    duraton_minutes = db.Column(db.Integer, default=60)
    status = db.Column(db.String(20), default='Scheduled') # scheduled, completed, cancelled
    notes = db.Column(db.Text)