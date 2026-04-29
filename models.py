from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ThermalAudit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    shade_percentage = db.Column(db.Float)
    risk_level = db.Column(db.String(20))

    def to_dict(self):
        return {
            "lat": self.lat, "lng": self.lng,
            "shade": self.shade_percentage, "risk": self.risk_level
        }