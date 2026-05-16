from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models.user import User
from app.models.trainer import Trainer
from app.models.client import Client

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])  # fixed methods list
def register():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'email already used'}), 400
    
    user = User(email=data['email'], role=data['role'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.flush()  # to get user.user_id

    if data['role'] == 'trainer':
        profile = Trainer(
            trainer_id=user.user_id,
            first_name=data['first_name'],
            last_name=data['last_name'],
            specialization=data.get('specialization', '')
        )
    else:  # client
        profile = Client(
            client_id=user.user_id,
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=data.get('phone'),
            trainer_id=data.get('trainer_id')
        )
    db.session.add(profile)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    # Use the model's check_password method if exists, else use werkzeug
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    access_token = create_access_token(identity=user.user_id)
    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user.user_id,
            'email': user.email,
            'role': user.role,
            'name': f"{profile.first_name} {profile.last_name}"  # need to fetch profile
        }
    }), 200