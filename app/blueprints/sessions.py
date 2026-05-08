from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.models import WorkoutSession, Trainer, User  # adjust import based on your __init__.py
from app.schemas.workout_plan_scheduler import WorkoutSessionSchema  # example schema
from app import db

sessions_bp = Blueprint('sessions', __name__)

@sessions_bp.route('/', methods=['GET'])
@jwt_required()
def get_sessions():
    """Get all workout sessions, optionally filtered by date"""
    date_str = request.args.get('date')
    query = WorkoutSession.query
    if date_str:
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            query = query.filter(WorkoutSession.date == date_obj)
        except:
            return jsonify({'error': 'Invalid date format'}), 400
    sessions = query.order_by(WorkoutSession.date, WorkoutSession.start_time).all()
    # Use schema to serialize if available, else manual
    schema = WorkoutSessionSchema(many=True)
    return jsonify(schema.dump(sessions))

@sessions_bp.route('/', methods=['POST'])
@jwt_required()
def create_session():
    """Only trainers can create sessions"""
    user_id = get_jwt_identity()
    trainer = Trainer.query.filter_by(user_id=user_id).first()
    if not trainer:
        return jsonify({'error': 'Only trainers can create sessions'}), 403
    
    data = request.json
    required = ['name', 'date', 'start_time', 'end_time', 'capacity']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing fields'}), 400
    
    try:
        date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()
        start = datetime.strptime(data['start_time'], '%H:%M').time()
        end = datetime.strptime(data['end_time'], '%H:%M').time()
    except:
        return jsonify({'error': 'Invalid date/time format'}), 400
    
    new_session = WorkoutSession(
        name=data['name'],
        trainer_id=trainer.id,
        date=date_obj,
        start_time=start,
        end_time=end,
        capacity=data['capacity'],
        booked_count=0
    )
    db.session.add(new_session)
    db.session.commit()
    return jsonify({'id': new_session.id, 'message': 'Session created'}), 201

@sessions_bp.route('/<int:session_id>', methods=['PUT'])
@jwt_required()
def update_session(session_id):
    user_id = get_jwt_identity()
    trainer = Trainer.query.filter_by(user_id=user_id).first()
    session = WorkoutSession.query.get_or_404(session_id)
    if not trainer or session.trainer_id != trainer.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    if 'name' in data:
        session.name = data['name']
    if 'capacity' in data:
        session.capacity = data['capacity']
    db.session.commit()
    return jsonify({'message': 'Session updated'})

@sessions_bp.route('/<int:session_id>', methods=['DELETE'])
@jwt_required()
def delete_session(session_id):
    user_id = get_jwt_identity()
    trainer = Trainer.query.filter_by(user_id=user_id).first()
    session = WorkoutSession.query.get_or_404(session_id)
    if not trainer or session.trainer_id != trainer.id:
        return jsonify({'error': 'Unauthorized'}), 403
    db.session.delete(session)
    db.session.commit()
    return jsonify({'message': 'Session deleted'})