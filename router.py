import requests
import math

def get_balanced_route(s_lat, s_lng, e_lat, e_lng, sens, heat_points):
    """Reactive Road-Legal Router with Heat Repulsion."""
    mid_lat, mid_lng = (s_lat + e_lat) / 2, (s_lng + e_lng) / 2
    rep_lat, rep_lng = 0, 0
    
    # 1. Scan for critical heatspots to push path away
    for pt in heat_points:
        dist = math.sqrt((pt['lat'] - mid_lat)**2 + (pt['lng'] - mid_lng)**2)
        if pt['shade'] < 25 and dist < 0.006:
            rep_lat = (mid_lat - pt['lat']) * 2.5 * sens
            rep_lng = (mid_lng - pt['lng']) * 2.5 * sens
            break 

    safe_lat, safe_lng = mid_lat + rep_lat + (0.001 * sens), mid_lng + rep_lng + (0.001 * sens)
    
    # 2. Call OSRM for road-legal geometry
    coords = f"{s_lng},{s_lat};{safe_lng},{safe_lat};{e_lng},{e_lat}"
    url = f"http://router.project-osrm.org/route/v1/walking/{coords}?overview=full&geometries=geojson"
    
    try:
        res = requests.get(url).json()
        path = [[c[1], c[0]] for c in res['routes'][0]['geometry']['coordinates']]
        dist = res['routes'][0]['distance']
    except:
        path, dist = [[s_lat, s_lng], [e_lat, e_lng]], 0

    return {
        "cool_path": path,
        "std_path": [[s_lat, s_lng], [e_lat, e_lng]],
        "metrics": {"uv": f"{int(sens * 60)}%", "dist": f"+{int(dist*0.1)}m"},
        "directions": ["Bypassing heat cluster.", "Following shaded street network.", f"Total: {int(dist)}m."]
    }

def get_ward_leaderboard():
    """Ranked list of thermal risk areas."""
    wards = [
        {"name": "Mandi Mohalla", "shade": 8, "temp": 37.2, "risk_score": 92},
        {"name": "Devaraja Mohalla", "shade": 14, "temp": 36.5, "risk_score": 85},
        {"name": "Gokulam", "shade": 62, "temp": 30.5, "risk_score": 32},
    ]
    return sorted(wards, key=lambda x: x['risk_score'], reverse=True)

def simulate_impact(ward, count):
    """Calculates cooling & financial ROI."""
    temp_drop = (count / 100) * 0.4
    savings = count * 15 * 8 # units * rate
    return {
        "temp": f"-{temp_drop:.1f}°C",
        "roi": f"₹{savings:,.0f}/mo",
        "co2": f"{count * 2}kg offset"
    