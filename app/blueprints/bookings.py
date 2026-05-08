from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import SessionBooking, WorkoutSession, Client
from app import db

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.rouute('/', methods=['GET'])
@jwt_required()
def get_user_bookings():
    user_id = get_jwt_identity()
    client = Client.query.filter_by(user_id=user_id).first()
    if not client:
        return jsonify({'error': 'Client profile not found'}), 404
    bookings = SessionBooking.query.filter_by(client_id=client.id).all()
    return jsonify([{
        'id': b.id,
        'sessionId': b.session_id,
        'sessionName': b.workout_session.name,
        'date': b.workout_sessin.date.isoformat(),
        'startTime': b.workout_session.start_time.strftime('%H:%M'),
        'trainer': b.workout_session.trainer.user.name # Assuming relationship
    } for b in bookings])

@bookings_bp.route('/', methods=['POST'])
@jwt_required()
def create_booking():
    user_id = get_jwt_identity()
    client = Client.query.filter_by(user_id=user_id).first()
    if not client:
        return jsonify({'error': 'Client profile not found'}), 404
    
    data = request.json
    session_id = data.get('session_id')
    if not session_id:
        return jsonify({'error': 'session_id required'}), 400
    
    session = WorkoutSession.query.get(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    
    # Check existing booking
    existing = SessionBooking.query.filter_by(client_id=client.id, session_id=session_id).first()
    if existing:
        return jsonify({'error': 'Already booked'}), 400
    
    # Check capacity
    if session.booked_count >= session.capacity:
        return jsonify({'error': 'Session is full'}), 400
    
    booking = SessionBooking(client_id=client.id, session_id=session_id)
    db.session.add(booking)
    session.booked_count += 1
    db.session.commit()
    
    return jsonify({'message': 'Booked successfully', 'bookingId': booking.id}), 201

@bookings_bp.route('/<int:booking_id>', methods=['DELETE'])
@jwt_required()
def cancel_booking(booking_id):
    user_id = get_jwt_identity()
    client = Client.query.filter_by(user_id=user_id).first()
    booking = SessionBooking.query.get_or_404(booking_id)
    if not client or booking.client_id != client.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    session = booking.workout_session
    db.session.delete(booking)
    session.booked_count -= 1
    db.session.commit()
    return jsonify({'message': 'Booking cancelled'})