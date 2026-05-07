from flask import Flask
import werkzeug.security
from .config import Config
from .extensions import db, jwt, ma, cors

def create_app(config_class=Config):
    app=Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

    # Register blueprints
    from .blueprints.auth import auth_bp
    from .blueprints.clients import clients_bp
    from .blueprints.trainers import trainers_bp
    from .blueprints.workouts import workouts_bp
    from .blueprints.bookings import bookings_bp
    from .blueprints.progress import progress_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(clients_bp, url_prefix='/api/clients')
    app.register_blueprint(trainers_bp, url_prefix='/api/trainers')
    app.register_blueprint(workouts_bp, url_prefix='/api/workouts')
    app.register_blueprint(bookings_bp, url_prefix='/api/bookings')
    app.register_blueprint(progress_bp, url_prefix='/api/progress')

    with app.app_context():
        db.create_all()

        return app