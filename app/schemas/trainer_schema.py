from ..extensions import ma
from ..models.trainer import Trainer

class TrainerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trainer
        load_instance = True