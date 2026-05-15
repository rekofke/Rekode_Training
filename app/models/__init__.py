from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import classes so they can be accessed via `from app.models import User, Client, ...`
from .user import User
from .client import Client
from .trainer import Trainer
from .workout_session import WorkoutSession
from .session_booking import SessionBooking
from .workout_plan import WorkoutPlan
from .workout_exercise import WorkoutExercise
from .progress_log import ProgressLog