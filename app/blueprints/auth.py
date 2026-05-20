from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db
from ..models.user import User
from ..models.trainer import Trainer
from ..models.client import Client

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400

    user = User(
        email=data['email'],
        role=data.get('role', 'client'),
        name=data['name'],
        password_hash=generate_password_hash(data['password'])
    )
    db.session.add(user)
    db.session.flush()

    if data['role'] == 'trainer':
        profile = Trainer(
            trainer_id=user.id,  # assuming Trainer.trainer_id references User.id
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            specialization=data.get('specialization', '')
        )
    else:
        profile = Client(
            user_id=user.id,  # Client.user_id references User.id
            name=data.get('name', ''),
            email=data['email'],
            phone=data.get('phone', ''),
            membership_type=data.get('membership_type', 'basic')
        )
    db.session.add(profile)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not check_password_hash(user.password_hash, data.get('password')):
        return jsonify({'error': 'Invalid credentials'}), 401
    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role
        }
    }), 200