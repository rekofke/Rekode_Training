from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.models.workout_session import WorkoutSession
from app.models.trainer import Trainer
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
    result = []
    for s in sessions:
        trainer_name = "Unknown"
        if s.trainer:
            trainer_name = f"{s.trainer.first_name} {s.trainer.last_name}"
        result.append({
            'id': s.id,
            'name': s.name,
            'trainer': trainer_name,
            'date': s.date.isoformat(),
            'startTime': s.start_time.strftime('%H:%M'),
            'endTime': s.end_time.strftime('%H:%M'),
            'capacity': s.capacity,
            'bookedCount': s.booked_count
        })
    return jsonify(result), 200

@sessions_bp.route('/', methods=['POST'])
@jwt_required()
def create_session():
    """Only trainers can create sessions"""
    user_id = get_jwt_identity()
    # Assuming Trainer model has a user_id foreign key; adjust as needed
    trainer = Trainer.query.filter_by(trainer_id=user_id).first()
    if not trainer:
        return jsonify({'error': 'Only trainers can create sessions'}), 403
    
    data = request.json
    required = ['name', 'date', 'startTime', 'endTime', 'capacity']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing fields'}), 400
    
    try:
        date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()
        start = datetime.strptime(data['startTime'], '%H:%M').time()
        end = datetime.strptime(data['endTime'], '%H:%M').time()
    except:
        return jsonify({'error': 'Invalid date/time format'}), 400
    
    new_session = WorkoutSession(
        name=data['name'],
        trainer_id=trainer.trainer_id,
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
    trainer = Trainer.query.filter_by(trainer_id=user_id).first()
    session = WorkoutSession.query.get_or_404(session_id)
    if not trainer or session.trainer_id != trainer.trainer_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    if 'name' in data:
        session.name = data['name']
    if 'capacity' in data:
        session.capacity = data['capacity']
    db.session.commit()
    return jsonify({'message': 'Session updated'}), 200

@sessions_bp.route('/<int:session_id>', methods=['DELETE'])
@jwt_required()
def delete_session(session_id):
    user_id = get_jwt_identity()
    trainer = Trainer.query.filter_by(trainer_id=user_id).first()
    session = WorkoutSession.query.get_or_404(session_id)
    if not trainer or session.trainer_id != trainer.trainer_id:
        return jsonify({'error': 'Unauthorized'}), 403
    db.session.delete(session)
    db.session.commit()
    return jsonify({'message': 'Session deleted'}), 200