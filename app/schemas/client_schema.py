from app.models.client import Client
from ..extensions import ma
from ..models import Client

class ClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Client
        load_instance = True
        include_fk = True