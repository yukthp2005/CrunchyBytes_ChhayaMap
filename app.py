import os
from flask import Flask, render_template, request, jsonify
from models import db, ThermalAudit
from vision_engine import analyze_thermal_threat, analyze_surface_albedo
from router import get_ward_leaderboard, get_thermal_route_data, simulate_impact

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chhaya.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-map-data')
def get_map_data():
    points = ThermalAudit.query.all()
    return jsonify([p.to_dict() for p in points])

@app.route('/get-leaderboard')
def get_leaderboard():
    return jsonify(get_ward_leaderboard())

@app.route('/get-cool-route')
def get_cool_route():
    s_lat = float(request.args.get('s_lat'))
    e_lat = float(request.args.get('e_lat'))
    sens = float(request.args.get('sens', 0.5))
    return jsonify(get_thermal_route_data(s_lat, 76.65, e_lat, 76.67, sens))

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    return jsonify(simulate_impact(data['ward'], int(data['count'])))

@app.route('/audit-albedo', methods=['POST'])
def audit_albedo():
    # In a live demo, process request.files['image']
    return jsonify({
        "albedo": 0.18, 
        "status": "CRITICAL HEAT TRAP",
        "roi": "₹12,400 annual cooling savings per building via White-Topping."
    })

@app.route('/bootstrap')
def bootstrap():
    db.create_all()
    if not ThermalAudit.query.first():
        seeds = [
            ThermalAudit(lat=12.3051, lng=76.6551, shade_percentage=5, risk_level="CRITICAL"),
            ThermalAudit(lat=12.3120, lng=76.6580, shade_percentage=10, risk_level="CRITICAL"),
            ThermalAudit(lat=12.2980, lng=76.6450, shade_percentage=60, risk_level="SAFE")
        ]
        db.session.add_all(seeds)
        db.session.commit()
    return "SYSTEM_BOOTSTRAPPED"

if __name__ == '__main__':
    app.run(debug=True, port=5000)