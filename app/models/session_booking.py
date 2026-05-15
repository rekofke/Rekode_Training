from ..extensions import db

class SessionBooking(db.Model):
    __tablename__ = 'session_bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('workout_sessions.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationships
    # No need for explicit relationship; the backref from WorkoutSession will provide it.