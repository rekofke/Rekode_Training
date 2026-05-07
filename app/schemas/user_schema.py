from ..extensions import ma
from ..models.user import User
from marshmallow import fields

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclued = ('password_hash')
    password = fields.string(load_only=True, required=True)

    