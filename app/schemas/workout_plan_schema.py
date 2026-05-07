from ..extensions import ma
from ..models.workout_plan import WorkoutPlan
from ..models.workout_exercise import WorkoutExercise
from marshmallow import fields

class WorkoutExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutExercise
        load_instance = True
        include_fk = True

class WorkoutPlanSchema(ma.SQLAlchemyAutoSchema):
    exercises = fields.List(fields.Nested(WorkoutExerciseSchema))
    class Meta:
        model = WorkoutPlan
        load_instance = True
        include_fk = True