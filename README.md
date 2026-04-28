# PROJECT CHHAYA: Tactical Thermal Intelligence
**Team: CrunchyBytes** *Building climate-resilient cities through Forensic Computer Vision.*

## 01. The Mission
CHHAYA is a community-driven platform designed to combat the Urban Heat Island (UHI) effect. By crowdsourcing street-level imagery, we use Computer Vision to audit urban shade and provide **Shade-Optimized Routing** for the gig economy and pedestrians.

## 02. Tech Stack
- **Backend:** Flask, SQLAlchemy (SQLite)
- **AI/CV:** OpenCV, NumPy (Shade segmentation & analysis)
- **Routing:** NetworkX (Thermal-weighted Dijkstra algorithm)
- **Frontend:** Leaflet.js, HTML5, CSS3 (Tactical High-Contrast UI)

## 03. Setup Instructions
1. Clone the repo: `git clone https://github.com/yukthp2005/CrunchyBytes_ChhayaMap.git`
2. Create VENV: `python -m venv venv`
3. Install: `pip install -r requirements.txt`
4. Run: `python app.py`
5. Access: `http://127.0.0.1:5000`

## 04. Demo Instructions
1. Click any location on the map to "Lock Target."
2. Upload a street-level photo.
3. Observe the CV Engine calculate the "Shade-to-Concrete" ratio.
4. View the real-time thermal bloom on the city-wide heatmap.