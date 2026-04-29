# Project CHHAYA: Thermal Intelligence Command Center

Project CHHAYA is a multi-layered urban resilience platform designed for high-density metropolitan environments. It transforms thermal data into actionable civic intelligence through reactive routing, forensic audits, and economic simulation.

## Core Intelligence Engines

### Reactive Thermal Navigation
- Road-Legal Logic: Integrated with the OSRM API to ensure pedestrian paths follow verified street networks, preventing routes from crossing through buildings or private property.
- Repulsion Vector Algorithm: Dynamically recalculates routes to avoid heat clusters detected in the audit database.
- Shade Sensitivity: A user-adjustable parameter that balances the trade-off between shortest distance and maximum thermal comfort.

### Forensic Albedo Audit
- Surface Intelligence: Uses Computer Vision (OpenCV) to analyze urban materials.
- Heat Trap Detection: Identifies low-albedo surfaces such as asphalt or dark tar that act as thermal batteries.

### Tree ROI Simulator
- Predictive Cooling: Simulates the temperature drop achieved by specific reforestation counts.
- Economic ROI: Quantifies monthly electricity savings in INR and CO2 offsets to provide a financial case for urban greening.

### Urban Risk Leaderboard
- Governance Tool: Ranks metropolitan wards based on a Climate Risk Index incorporating temperature, shade density, and canopy percentage.

## Tech Stack
- Backend: Python (Flask), SQLAlchemy (SQLite)
- Mapping: Leaflet.js, Leaflet.heat
- Routing: Open Source Routing Machine (OSRM) API
- Intelligence: OpenCV, NumPy, Requests

## Setup and Execution

1. Install Dependencies:
   pip install -r requirements.txt

2. Initialize and Launch:
   python app.py

3. Access Dashboard:
   http://127.0.0.1:5000

Developed by Team CrunchyBytes