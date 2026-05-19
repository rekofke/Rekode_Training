from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.user import User
from ..models.client import Client
from ..models.trainer import Trainer


clients_bp = Blueprint('clients', __name__)


@clients_bp.route('/', methods=['GET'])
@jwt_required()
def get_clients():
    """Get all clients acceessible to the current user
    - If user is trainer: return all clients assigned to that trainer
    - If user is client: return their own client profile
    - If user is admin: return all cients (if needed)
    """
    clients = Client.query.filter_by(...).all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'email': c.email,
        'phone': c.phone
    } for c in clients])


    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({'error:' 'User not found'}), 404
    
    if user.role == 'Trainer':
        # Assume Trainer model has a relationship to Client via trainer_id
        trainer = Trainer.query.filter_by(user_id=current_user_id).first()
        if not trainer:
            return jsonify({'error': 'Trainer profile not found'}), 404
        clients = Client.query.filter_by(trainer_id=trainer.id).all()
    elif user.role == 'client':
        # Client has direct client profile linked to their user_id
        client = Client.query.filter_by(user_id=current_user_id).first()
        

