import os
import time
import cv2
import numpy as np
from ultralytics import YOLO
# from flask import Flask, render_template, Response, jsonify

# YOLO 모델 로드
model = YOLO('best.pt')

# app = Flask(__name__)

# "drowsy" 감지 시간 저장을 위한 리스트
drowsy_detections = []

def gen_frames():
    cap = cv2.VideoCapture(0)  # 웹캠 사용 (0번 카메라)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        success, frame = cap.read()
        if not success:
            break
        
        results = model(frame)

        # 현재 시간
        current_time = time.time()
        global drowsy_detections

        for result in results:
            for box in result.boxes:
                if 'Drowsy' in result.names[int(box.cls)]:
                    drowsy_detections.append(current_time)
                    # 10초가 지난 감지 시간은 리스트에서 제거
                    drowsy_detections = [t for t in drowsy_detections if current_time - t <= 10]
                    break
            
            annotated_frame = result.plot()

        # 프레임 크기 조정 (1000x1000)
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
