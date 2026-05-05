from ultralytics import YOLO
from picamera2 import Picamera2
import time
import cv2

from config.settings import *
from perception.node_detection import detect_node_color
from perception.lane_detection import compute_steering
from perception.object_detection import detect_traffic_stop
from control.serial_comm import init_serial, send_control
from utils.visualization import draw_steering_gauge
from perception.aruco_detection import detect_aruco_marker
def main():
    print("[info] khoi tao mo hinh va camera...")
    lane_model = YOLO(lane_model_path, task="segment")
    obj_model = YOLO(obj_model_path, task="detect")
    try:
        ser = serial.Serial(serial_port, baud_rate, timeout=0)
        time.sleep(2)
    except:
        print("[warn] khong the ket noi serial!")
        ser = None
 
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"size": (frame_width, frame_height), "format": "BGR888"})
    picam2.configure(config)
    picam2.start()
    try:
        target_marker = int(input("=> nhap id marker dich: "))
    except:
        target_marker = 0
 
    cam_x = frame_width // 2
    cam_y = frame_height
    roi_top = int(frame_height * (1 - roi_ratio))
    angle_deg = 0
    frame_counter = 0
    is_running = True
    should_stop_for_traffic = False
    traffic_reason = ""
    start_time = time.time()
    fps_start = time.time()
    fps_count = 0
    fps_val = 0
 
    try:
        while True:
            frame = picam2.capture_array()
            if frame is None: continue
            # Khởi tạo frame hiển thị
            annotated_frame = frame.copy()
            # 1. Kiem tra aruco marker
            curr_m = detect_aruco_marker(frame, annotated_frame)
            if curr_m == target_marker and (time.time() - start_time > 2.0):
                is_running = False
                print(f"[stop] da den dich: {target_marker}")
 
            # 2. Xu ly vat the (skip_obj = 5) - Quét toàn bộ khung hình
            if frame_counter % skip_obj == 0:
                obj_res = obj_model.predict(source=frame, imgsz=img_size, conf=0.2, verbose=False)
                should_stop_for_traffic = False
                traffic_reason = ""
                for box in obj_res[0].boxes:
                    c_id = int(box.cls[0])
                    name = obj_model.names[c_id].lower()
                    if "red" in name or "stop" in name:
                        should_stop_for_traffic = True
                        traffic_reason = name
                        # Đã xóa phần vẽ cv2.rectangle và hiển thị tên object để tối ưu FPS
 
            # 3. Xu ly lan duong (skip_lane = 2) - Chỉ quét vùng ROI
            if frame_counter % skip_lane == 0:
                roi_frame = frame[roi_top:, :]
                lane_res = lane_model.predict(source=roi_frame, imgsz=img_size, conf=0.2, verbose=False)
                masks = lane_res[0].masks
                if masks is not None and len(masks.xy) > 0:
                    pts = []
                    for poly in masks.xy:
                        if len(poly) > 0:
                            c = get_centroid(np.array(poly, dtype=np.int32))
                            if c: pts.append((c[0], c[1] + roi_top))
                    if len(pts) > 0:
                        pts.sort(key=lambda p: p[0])
                        if len(pts) >= 2:
                            tx, ty = (pts[-2][0]+pts[-1][0])//2, (pts[-2][1]+pts[-1][1])//2
                        else:
                            tx = pts[0][0] - 100 if pts[0][0] > cam_x else pts[0][0] + 100
                            ty = pts[0][1]
                        dx, dy = tx - cam_x, cam_y - ty
                        angle_deg = int(math.degrees(math.atan2(dx, dy if dy != 0 else 1)))
                        # Vẫn giữ lại điểm chấm (điểm đích) để nhìn góc lái dễ hơn, không tốn nhiều FPS
                        cv2.circle(annotated_frame, (tx, ty), 8, (0, 0, 255), -1)
 
            # 4. Dieu khien serial
            if ser:
                m_cmd = 1 if (is_running and not should_stop_for_traffic) else 0
                ser.write(f"{angle_deg},{m_cmd}\n".encode('utf-8'))
 
            # 5. Hien thi thong tin co ban
            draw_steering_gauge(annotated_frame, angle_deg)
            fps_count += 1
            if time.time() - fps_start > 1.0:
                fps_val = fps_count / (time.time() - fps_start)
                fps_count, fps_start = 0, time.time()
 
            status = "run" if is_running else "stop"
            if should_stop_for_traffic: status = f"halt:{traffic_reason}"
            cv2.putText(annotated_frame, f"fps:{fps_val:.1f} | {status}", (10, 25), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            cv2.imshow("car_control", annotated_frame)
            frame_counter += 1
            if cv2.waitKey(1) & 0xff == ord('q'): break
 
    finally:
        if ser:
            ser.write(b"0,0\n")
            ser.close()
        picam2.stop()
        cv2.destroyAllWindows()
 
if __name__ == "__main__":
    main()