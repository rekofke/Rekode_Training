from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from .extensions import db

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Register root route
    @app.route('/')
    def home():
        return {"message": "Rekode Fitness API is running"}
    
    # Import and register blueprints
    from app.blueprints.auth import auth_bp
    from app.blueprints.clients import clients_bp
    from app.blueprints.sessions import sessions_bp
    from app.blueprints.bookings import bookings_bp
    from app.blueprints.workouts import workouts_bp
    from app.blueprints.progress import progress_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(clients_bp, url_prefix='/api/clients')
    app.register_blueprint(sessions_bp, url_prefix='/api/sessions')
    app.register_blueprint(bookings_bp, url_prefix='/api/bookings')
    app.register_blueprint(workouts_bp, url_prefix='/api/workouts')
    app.register_blueprint(progress_bp, url_prefix='/api/progress')
    
    with app.app_context():
        db.create_all()
    
    return app