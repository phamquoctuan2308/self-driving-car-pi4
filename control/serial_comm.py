import serial
import time
from config.settings import SERIAL_PORT, BAUD_RATE

def init_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0)
        time.sleep(2)
        return ser
    except:
        print("[WARN] Serial failed")
        return None

def send_control(ser, angle, run):
    if ser:
        msg = f"{angle},{1 if run else 0}\n"
        ser.write(msg.encode())