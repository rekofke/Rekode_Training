from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.client import Client
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

        user = User(email=data['email'], role=data['role'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.flush()

        if data['role'] == 'trainer':
            profile = trainer(
                trainer_id=user.user_id,
                first_name=data['first_name'],
                last_name=data['last_name'],
                specialization=data.get('specialization', '') 
            )
        else:
            profile = Client(
                client_id=user.user_id,
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone=data.get('phone'),
                trainer_id=data.get('trainer_id') 
            )
        db.session.data(profile)
        db.session.commit()
        return jsonify({'message': 'User created'}), 201

    @auth_bp.route('/login', methods=['POST'])
    def login():
        data = request.json
        user = User.query.filter_by(email=data['email']).first()
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        token = create_access_token(identify=user.user_id)
        return jsonify({'access_token': token, 'role': user.role}), 200
