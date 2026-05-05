import numpy as np
import math
import cv2

def get_centroid(polygon):
    M = cv2.moments(polygon)
    if M['m00'] != 0:
        return int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    return None

