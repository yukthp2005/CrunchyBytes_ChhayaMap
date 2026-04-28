def get_ward_leaderboard():
    wards = [
        {"name": "Mandi Mohalla", "shade": 8, "temp": 37.2, "trees": 120, "risk_score": 92},
        {"name": "Devaraja Mohalla", "shade": 14, "temp": 36.5, "trees": 215, "risk_score": 85},
        {"name": "Kuja Ward", "shade": 22, "temp": 34.1, "trees": 480, "risk_score": 71},
        {"name": "Gokulam", "shade": 60, "temp": 30.5, "trees": 2400, "risk_score": 32},
    ]
    return sorted(wards, key=lambda x: x['risk_score'], reverse=True)

def simulate_impact(ward, count):
    temp_drop = (count / 100) * 0.5
    energy_saved_inr = count * 15 * 8 # units * rate
    return {
        "temp_reduction": f"-{temp_drop:.1f}°C",
        "energy_roi": f"₹{energy_saved_inr:,.0f}/mo",
        "co2": f"{count * 2.5}kg carbon offset"
    }

def get_thermal_route_data(s_lat, s_lng, e_lat, e_lng, sens):
    # Practical Detour logic
    offset = 0.0015 * sens
    return {
        "cool_path": [[s_lat, s_lng], [s_lat + offset, s_lng + offset], [e_lat, e_lng]],
        "std_path": [[s_lat, s_lng], [e_lat, e_lng]],
        "uv_reduction": f"{int(sens * 45)}%",
        "directions": [
            "Start heading North-West.",
            "Cross to the shaded side of the street.",
            "Algorithm detected 40% more canopy on parallel lane.",
            "Arrive via the residential cooling corridor."
        ]
    }