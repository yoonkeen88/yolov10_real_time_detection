from flask import Blueprint, render_template, Response, current_app, redirect, request, send_file
from flask_socketio import SocketIO, emit
import os
import time
import cv2
from ultralytics import YOLO
# from .utils import gen_frames, process_video
from werkzeug.utils import secure_filename

# Initialize SocketIO
socketio = SocketIO()
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/webcam')
def webcam():
    return render_template('webcam.html')

@main.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
# YOLO 모델 로드
model = YOLO('best.pt')

# "drowsy" 감지 시간 저장을 위한 리스트를 모듈 수준에서 선언
drowsy_detections = []

# def gen_frames():
#     cap = cv2.VideoCapture(0)  # 웹캠 인덱스
#     if not cap.isOpened():
#         print("Error: Could not open webcam.")
#         return

#     while True:
#         success, frame = cap.read()

#         if not success:
#             break

#         # YOLO 모델로 프레임을 처리합니다.
#         results = model(frame)

#         # 결과를 시각화합니다.
#         annotated_frame = results[0].plot()  # 결과의 첫 번째 이미지에 대한 플롯을 얻음

#         # 프레임 크기 조정 (1000x1000)
#         annotated_frame = cv2.resize(annotated_frame, (1000, 1000))
#         ret, buffer = cv2.imencode('.jpg', annotated_frame)
#         frame = buffer.tobytes()

#         # 프레임 전송
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#     cap.release()
def gen_frames():
    cap = cv2.VideoCapture(0)  # 웹캠 인덱스
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        success, frame = cap.read()

        if not success:
            print("Failed to read frame.")
            break

        results = model(frame)
        
        # 모델 결과의 구조 확인
        if isinstance(results, list) and len(results) > 0:
            predictions = results[0]
        elif isinstance(results, dict):
            predictions = results.get('pred')  # 'pred' 키로 데이터를 가져옴
        else:
            print("Unexpected results structure")
            continue

        # predictions의 구조 확인
        if isinstance(predictions, list) and len(predictions) > 0:
            annotated_frame = predictions[0].plot()  # 일반적인 경우
        else:
            print("No valid predictions found.")
            continue

        # 프레임 크기 조정 (1000x1000)
        annotated_frame = cv2.resize(annotated_frame, (1000, 1000))
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        if not ret:
            print("Failed to encode frame.")
            continue
        frame = buffer.tobytes()

        # 프레임 전송
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    print("Capture released.")



@main.route('/upload')
def upload():
    return render_template('upload.html')

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # Process the video file and save the result
        processed_video_path = process_video(filepath)
        return send_file(processed_video_path, as_attachment=True)
    return redirect(request.url)
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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
