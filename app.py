import os
from flask import Flask, render_template, request, jsonify
from models import db, ThermalAudit
from vision_engine import analyze_thermal_threat

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chhaya.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report-heat', methods=['POST'])
def report_heat():
    try:
        file = request.files['image']
        lat = float(request.form['lat'])
        lng = float(request.form['lng'])
        
        filename = f"{lat}_{lng}_{file.filename}"
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        
        shade, risk = analyze_thermal_threat(path)
        
        new_audit = ThermalAudit(
            lat=lat, lng=lng, shade_percentage=shade, 
            risk_level=risk, image_path=path
        )
        db.session.add(new_audit)
        db.session.commit()
        
        return jsonify({"status": "SUCCESS", "risk": risk, "shade": shade})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 400

@app.route('/get-map-data')
def get_map_data():
    points = ThermalAudit.query.all()
    return jsonify([p.to_dict() for p in points])

if __name__ == '__main__':
    app.run(debug=True, port=5000)