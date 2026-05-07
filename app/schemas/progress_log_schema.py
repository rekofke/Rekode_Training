from ..extensions import ma
from ..models.progress_log import ProgressLog

class ProgressLogsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProgressLog
        load_instance = True
        include_fk = True