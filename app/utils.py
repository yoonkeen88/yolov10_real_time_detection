import cv2
import numpy as np
from ultralytics import YOLO
import os

# Load your YOLO model here
model = YOLO('/Users/angwang-yun/Desktop/Project/yolov10_real_time_detection/yolov10/yolov10n.pt')

def gen_frames():
    cap = cv2.VideoCapture(0)  # Use 0 for webcam
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return  # �쎒罹좎쓣 �뿴 �닔 �뾾�뒗 寃쎌슦 �븿�닔 醫낅즺
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        results = model(frame)
        # YOLOv8 �씠�썑 踰꾩쟾�뿉�꽌�뒗 �씠誘몄���뿉 吏곸젒 洹몃━湲�
        for result in results:
            annotated_frame = result.plot()  # result.render() ����떊 result.plot() �궗�슜
        # Resize frame to 1000x1000
        annotated_frame = cv2.resize(annotated_frame, (1000, 1000))
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def process_video(filepath):
    # Create output file path
    output_filepath = os.path.splitext(filepath)[0] + '_processed.mp4'
    
    # Open video file
    cap = cv2.VideoCapture(filepath)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_filepath, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)
        annotated_frame = results.render()[0]
        out.write(annotated_frame)

    cap.release()
    out.release()
    return output_filepath
