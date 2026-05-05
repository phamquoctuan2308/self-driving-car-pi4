import os
os.environ['OPENBLAS_CORETYPE'] = 'ARMV8'

# --- CẤU HÌNH HỆ THỐNG ---
os.environ['OPENBLAS_CORETYPE'] = 'ARMV8'
base_dir = os.path.dirname(os.path.abspath(__file__))
lane_model_path = "/home/tuan/code/seg_ncnn_model"
obj_model_path = "/home/tuan/Desktop/detect1_ncnn_model"
img_size = 320
frame_width = 320
frame_height = 240
serial_port = '/dev/ttyUSB0'
baud_rate = 9600
 
# --- CẤU HÌNH TỐI ƯU FPS ---
skip_lane = 2  # Cập nhật: Nhận diện đường mỗi 2 frame
skip_obj = 5   # Nhận diện vật thể mỗi 5 frame
roi_ratio = 0.5  # Lấy 50% phần dưới khung hình để quét làn đường
 
marker_history = deque(maxlen=5)