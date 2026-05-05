import numpy as np
import math
import cv2
def compute_steering(masks, cam_x, cam_y, last_angle):
    if masks is None or len(masks.xy) == 0:
        return last_angle, None

    centroids = []
    for poly in masks.xy:
        poly_int = np.array(poly, dtype=np.int32)
        c = get_centroid(poly_int)
        if c: centroids.append(c)

    if not centroids:
        return last_angle, None

    centroids.sort(key=lambda p: p[0])

    if len(centroids) >= 2:
        l, r = centroids[-2], centroids[-1]
        target_x = (l[0] + r[0]) // 2
        target_y = (l[1] + r[1]) // 2
    else:
        single = centroids[0]
        target_y = single[1]
        target_x = single[0] - 125 if single[0] > cam_x else single[0] + 125

    dx = target_x - cam_x
    dy = cam_y - target_y if cam_y - target_y != 0 else 1

    angle = int(math.degrees(math.atan(dx / dy)))
    return angle, (target_x, target_y)