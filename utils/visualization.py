import cv2
import math

def draw_steering_gauge(img, angle, center=(160, 80), radius=60):
    cv2.ellipse(img, center, (radius, radius), 180, 0, 180, (200, 200, 200), 2)
    angle_rad = math.radians(angle)
    end_x = int(center[0] + radius * math.sin(angle_rad))
    end_y = int(center[1] - radius * math.cos(angle_rad))
    # logic màu sắc: xanh (<15), vàng (<35), đỏ (>=35)
    if abs(angle) < 15: color = (0, 255, 0)
    elif abs(angle) < 35: color = (0, 255, 255)
    else: color = (0, 0, 255)
    cv2.line(img, center, (end_x, end_y), color, 4)
    cv2.circle(img, center, 6, (255, 255, 255), -1)