def detect_traffic_stop(results, model):
    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        name = model.names[cls_id].lower()
        if "red" in name or "stop" in name:
            return True, name.upper()
    return False, ""