import cv2
import numpy as np

def analyze_thermal_threat(image_path):
    img = cv2.imread(image_path)
    if img is None: return 0, "VOID"

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Target low 'Value' pixels (Shadows)
    lower_shadow = np.array([0, 0, 0])
    upper_shadow = np.array([180, 255, 85]) 
    
    mask = cv2.inRange(hsv, lower_shadow, upper_shadow)
    shade_px = cv2.countNonZero(mask)
    total_px = img.shape[0] * img.shape[1]
    
    shade_pct = (shade_px / total_px) * 100
    
    if shade_pct < 15: risk = "CRITICAL"
    elif shade_pct < 40: risk = "MODERATE"
    else: risk = "SAFE"
        
    return round(shade_pct, 2), risk