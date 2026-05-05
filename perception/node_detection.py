import cv2
import numpy as np
from collections import deque
from config.settings import FRAME_HEIGHT

node_history = deque(maxlen=5)

def detect_node_color(frame):
    roi = frame[FRAME_HEIGHT // 2 : FRAME_HEIGHT, :]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (5,5), 0)

    kernel = np.ones((5,5), np.uint8)

    def get_best_contour(mask):
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        best, max_area = None, 1000
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 1500 and area > max_area:
                best = cnt
                max_area = area
        return best

    red_mask = cv2.inRange(hsv, (0,120,70), (10,255,255)) + cv2.inRange(hsv, (170,120,70), (180,255,255))
    green_mask = cv2.inRange(hsv, (40,100,50), (90,255,255))
    yellow_mask = cv2.inRange(hsv, (20,100,100), (35,255,255))
    blue_mask = cv2.inRange(hsv, (100,150,0), (140,255,255))

    red_cnt = get_best_contour(red_mask)
    green_cnt = get_best_contour(green_mask)
    yellow_cnt = get_best_contour(yellow_mask)
    blue_cnt = get_best_contour(blue_mask)

    h, w, _ = roi.shape

    def is_center(cnt):
        x, y, cw, ch = cv2.boundingRect(cnt)
        cx = x + cw // 2
        return (w//3 < cx < 2*w//3)

    node = 0
    if red_cnt is not None and is_center(red_cnt): node = 1
    elif green_cnt is not None and is_center(green_cnt): node = 2
    elif yellow_cnt is not None and is_center(yellow_cnt): node = 3
    elif blue_cnt is not None and is_center(blue_cnt): node = 4

    if node != 0:
        node_history.append(node)
        if node_history.count(node) >= 3:
            node_history.clear()
            return node

    return 0
def detect_aruco_marker(frame, annotated_frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    try:
        # dành cho opencv mới
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        parameters = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
        corners, ids, rejected = detector.detectMarkers(gray)
    except AttributeError:
        # dành cho opencv cũ
        aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
        parameters = cv2.aruco.DetectorParameters_create()
        corners, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
 
    if ids is not None and len(ids) > 0:
        # Giữ lại vẽ Aruco để debug điểm dừng, không ảnh hưởng nhiều tới FPS
        cv2.aruco.drawDetectedMarkers(annotated_frame, corners, ids)
        marker_id = int(ids[0][0])
        marker_history.append(marker_id)
        if marker_history.count(marker_id) >= 2:
            marker_history.clear()
            return marker_id
    return -1