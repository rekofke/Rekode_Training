from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.user import User
from ..models.client import Client
from ..models.trainer import Trainer
from ..schemas.client_schema import ClientSchema

clients_bp = Blueprint('clients', __name__)
client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)

@clients_bp.route('/', methods=['GET'])
@jwt_required()
def get_clients():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user.role == 'trainer':
        trainer = Trainer.query.get(current_user_id)
        clients = Client.query.filter_by(trainer_id=trainer.trainer_id).all()
    else:
        clients = Client.query.filter_by(client_id=current_user_id).all()
    return clients_schema.jsonify(clients), 200

@clients_bp.route  

