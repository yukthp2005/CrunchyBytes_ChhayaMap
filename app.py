import os
from flask import Flask, render_template, request, jsonify
from models import db, ThermalAudit
from vision_engine import analyze_thermal_threat
from router import get_balanced_route, get_ward_leaderboard, simulate_impact

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chhaya.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-cool-route')
def get_cool_route():
    s_lat, s_lng = float(request.args.get('s_lat')), float(request.args.get('s_lng'))
    e_lat, e_lng = float(request.args.get('e_lat')), float(request.args.get('e_lng'))
    sens = float(request.args.get('sens', 0.5))
    all_points = [p.to_dict() for p in ThermalAudit.query.all()]
    return jsonify(get_balanced_route(s_lat, s_lng, e_lat, e_lng, sens, all_points))

@app.route('/get-leaderboard')
def get_leaderboard():
    return jsonify(get_ward_leaderboard())

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    return jsonify(simulate_impact(data['ward'], int(data['count'])))

@app.route('/report-heat', methods=['POST'])
def report_heat():
    lat, lng = float(request.form['lat']), float(request.form['lng'])
    new_audit = ThermalAudit(lat=lat, lng=lng, shade_percentage=10, risk_level="CRITICAL")
    db.session.add(new_audit)
    db.session.commit()
    return jsonify({"status": "SUCCESS"})

@app.route('/get-map-data')
def get_map_data():
    return jsonify([p.to_dict() for p in ThermalAudit.query.all()])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)