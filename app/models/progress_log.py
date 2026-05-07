from ..extensions import db

class ProgressLog(db.Model):
    __tablename__ = 'progress_logs'
    log_id  = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    date = db.Column(db.Date, server_default-db.func.current_date())
    weight_kg = db.Column(db.Numberic(5, 2))
    body_fat_percentage = db.Column(db.Numberic(4, 2))
    Measurements = db.Column(db.JSON) # EG {"chest":100, "waist":80, "hips":90}
    notes = db.Column(db.Text)