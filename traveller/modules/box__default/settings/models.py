from init import db
from shopyo.api.models import PkModel


class Settings(PkModel):
    __tablename__ = "settings"
    
    setting = db.Column(db.String(100))
    value = db.Column(db.String(100))