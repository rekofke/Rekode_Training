from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.columb(db.Integer, primary_key=True)
    email = db.column(db.String(120), unique=True, nullable=False)
    passwrd_hash = db.column(db.String(120), nullable=False)
    role = db.column(db.String(120),nullable=False) # 'Trainer' or 'Client'
    created_at = db.column(db.DateTime, server_default=db.func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

