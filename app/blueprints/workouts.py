from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import WorkoutPlan, WorkoutExercise, Trainer
from app import db

workouts_bp = Blueprint('workouts', __name__)

#______Workout Plans______#
@workouts_bp.route('/sessions', methods=['GET'])
@jwt_required()
def get_workout_plans():
    user_id = get_jwt_identity()
    trainer = Trainer.query.filter_by(user_id=user_id).first()
    if not trainer:
        return jsonify({'error': 'Only trainers can access'}), 403
    plans = WorkoutPlan.query.filter_by(trainer_id=trainer.id).all()
    return jsonify([{'id': p.id, 'name': p.name, 'description': p.description} for p in plans])

@workouts_bp.route('/plans', methods=['POST'])
@jwt_required()
def create_workout_plan():
    user_id = get_jwt_identity()
    trainer = Trainer.query.filter_by(user_id=user_id).first()
    if not trainer:
        return jsonify({'error': 'Only trainers can access'}), 403
    data = request.json
    plan = WorkoutPlan(name=data['name'], description=data.get('description'), trainer_id=trainer.id)
    db.session.add(plan)
    db.session.commit()
    return jsonify({'id': plan.id, 'message': 'Plan created'}), 201

@workouts_bp.route('/plans/<int:plan_id>/exercises', methods=['POST'])
@jwt_required()
def add_exercise_to_plan(plan_id):
    user_id = get_jwt_identity()
    trainer = Trainer.query.filter_by(user_id=user_id).first()
    plan = WorkoutPlan.query.get_or_404(plan_id)
    if plan.trainer_id != trainer.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    exercise = WorkoutExercise(
        workout_plan_id=plan_id,
        name=data['name'],
        sets=data['sets'],
        reps=data['reps'],
        rest_seconds=data.get('rest_seconds')
    )
    db.session.add(exercise)
    db.session.commit()
    return jsonify({'id': exercise.id, 'message': 'Exercise added'})