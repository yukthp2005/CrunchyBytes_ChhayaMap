from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ThermalAudit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    shade_percentage = db.Column(db.Float)
    risk_level = db.Column(db.String(20))
    image_path = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "lat": self.lat,
            "lng": self.lng,
            "intensity": 100 - self.shade_percentage, 
            "risk": self.risk_level,
            "shade": self.shade_percentage
        }
