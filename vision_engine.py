import cv2
import numpy as np

def analyze_thermal_threat(image_path):
    img = cv2.imread(image_path)
    if img is None: return 0, "UNKNOWN"
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, shadow_mask = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)
    shade_perc = (np.sum(shadow_mask == 255) / shadow_mask.size) * 100
    risk = "CRITICAL" if shade_perc < 20 else "MODERATE" if shade_perc < 50 else "SAFE"
    return round(shade_perc, 1), risk

def analyze_surface_albedo(image_path):
    img = cv2.imread(image_path)
    if img is None: return 0.2, "HEAT TRAP"
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    albedo = round(np.mean(gray) / 255.0, 2)
    status = "HEAT TRAP" if albedo < 0.3 else "COOL SURFACE" if albedo > 0.7 else "NEUTRAL"
    return albedo, statu