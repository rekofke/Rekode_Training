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
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.role == 'trainer':
        trainer = Trainer.query.filter_by(user_id=current_user_id).first()
        if not trainer:
            return jsonify({'error': 'Trainer profile not found'}), 404
        clients = Client.query.filter_by(trainer_id=trainer.id).all()
    else:  # client
        clients = Client.query.filter_by(user_id=current_user_id).all()

    # Manual serialization
    result = [{
        'id': c.id,
        'user_id': c.user_id,
        'trainer_id': c.trainer_id,
        'name': c.name,
        'email': c.email,
        'phone': c.phone,
        'membership_type': c.membership_type
    } for c in clients]
    return jsonify(result), 200

@clients_bp.route('/', methods=['POST'])
@jwt_required()
def create_client():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data'}), 400

    # For trainers: allow creating a client for another user
    if user.role == 'trainer':
        trainer = Trainer.query.filter_by(user_id=current_user_id).first()
        if not trainer:
            return jsonify({'error': 'Trainer profile not found'}), 404
        # Expected: user_id, name, email, phone, membership_type
        client_user_id = data.get('user_id')
        if not client_user_id:
            return jsonify({'error': 'user_id required'}), 400
        # Ensure that user exists and has role 'client'
        client_user = User.query.get(client_user_id)
        if not client_user or client_user.role != 'client':
            return jsonify({'error': 'Invalid client user_id'}), 400
        # Check if client profile already exists
        if Client.query.filter_by(user_id=client_user_id).first():
            return jsonify({'error': 'Client profile already exists'}), 400
        new_client = Client(
            user_id=client_user_id,
            trainer_id=trainer.id,
            name=data.get('name', client_user.name),
            email=data.get('email', client_user.email),
            phone=data.get('phone', ''),
            membership_type=data.get('membership_type', 'basic')
        )
        db.session.add(new_client)
        db.session.commit()
        return jsonify({'id': new_client.id, 'message': 'Client created'}), 201

    # For regular user (client) creating their own profile
    elif user.role == 'client':
        if Client.query.filter_by(user_id=current_user_id).first():
            return jsonify({'error': 'Client profile already exists'}), 400
        new_client = Client(
            user_id=current_user_id,
            name=data.get('name', user.name),
            email=data.get('email', user.email),
            phone=data.get('phone', ''),
            membership_type=data.get('membership_type', 'basic')
        )
        db.session.add(new_client)
        db.session.commit()
        return jsonify({'id': new_client.id, 'message': 'Client profile created'}), 201

    else:
        return jsonify({'error': 'Insufficient permissions'}), 403

@clients_bp.route('/<int:client_id>', methods=['PUT'])
@jwt_required()
def update_client(client_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404

    # Authorization
    if user.role == 'trainer':
        trainer = Trainer.query.filter_by(user_id=current_user_id).first()
        if not trainer or client.trainer_id != trainer.id:
            return jsonify({'error': 'Unauthorized'}), 403
    elif user.role == 'client':
        if client.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403
    else:
        return jsonify({'error': 'Forbidden'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data'}), 400

    if 'name' in data:
        client.name = data['name']
    if 'email' in data:
        client.email = data['email']
    if 'phone' in data:
        client.phone = data['phone']
    if 'membership_type' in data:
        client.membership_type = data['membership_type']
    db.session.commit()
    return jsonify({'id': client.id, 'message': 'Client updated'}), 200

@clients_bp.route('/<int:client_id>', methods=['DELETE'])
@jwt_required()
def delete_client(client_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404

    if user.role == 'trainer':
        trainer = Trainer.query.filter_by(user_id=current_user_id).first()
        if not trainer or client.trainer_id != trainer.id:
            return jsonify({'error': 'Unauthorized'}), 403
        db.session.delete(client)
        db.session.commit()
        return jsonify({'message': 'Client deleted'}), 200
    elif user.role == 'admin':
        db.session.delete(client)
        db.session.commit()
        return jsonify({'message': 'Client deleted by admin'}), 200
    else:
        return jsonify({'error': 'Only trainer or admin can delete clients'}), 403