from ..extensions import db
from sqlalchemy import func

class ProgressLog(db.Model):
    __tablename__ = 'progress_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    date = db.Column(db.Date, server_default=func.current_date())
    weight = db.Column(db.Float)
    body_fat = db.Column(db.Float)
    notes = db.Column(db.Text)
    
    # No explicit relationship; the backref from Client.progress_logs provides 'client'