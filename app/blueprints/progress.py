from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import ProgressLog, Client
from app import db

progress_bp = Blueprint('progress', __name__)

@progress_bp.route('/', methods=['GET'])
@jwt_required()
def get_progress_logs():
    user_id = get_jwt_identity()
    client = Client.query.filter_by(user_id=user_id).first()
    if not client:
        return jsonify({'error': 'Client profile not found'}), 404
    logs = ProgressLog.query.filter_by(client_id=client.id).order_by(ProgressLog.date.desc()).all()
    return jsonify([{
        'id': l.id,
        'date': l.date.isoformat(),
        'weight': l.weight,
        'body_fat': l.body_fat,
        'notes': l.notes
    } for l in logs])

@progress_bp.route('/', methods=['POST'])
@jwt_required()
def add_progress_log():
    user_id = get_jwt_identity()
    client = Client.query.filter_by(user_id=user_id).first()
    if not client:
        return jsonify({'error': 'Client profile not found'}), 404
    
    data = request.json
    log = ProgressLog(
        client_id=client.id,
        weight=data.get('weight'),
        body_fat=data.get('body_fat'),
        notes=data.get('notes')
    )
    db.session.add(log)
    db.session.commit()
    return jsonify({'id': log.id, 'message': 'Progress logged'}), 201
