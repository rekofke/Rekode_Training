from ..extensions import ma
from ..models.session_booking import SessionBooking

class SessionBookingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SessionBooking
        load_instanc = True
        include_fk = True