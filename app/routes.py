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

def gen_frames():
    cap = cv2.VideoCapture(0)  # 웹캠 인덱스
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

        for result in results:
            for box in result.boxes:
                # 클래스 이름과 확률을 추출
                class_name = result.names[int(box.cls)]
                confidence = box.conf.item()  # Tensor를 Python 숫자로 변환
                label = f"{class_name} {confidence:.2f}"

                # "Drowsy"가 감지되었는지 확인
                if "Drowsy" in label:
                    drowsy_detections.append(current_time)
                    # 10초가 지난 감지 시간은 리스트에서 제거
                    drowsy_detections[:] = [t for t in drowsy_detections if current_time - t <= 10]
                    break
            
            annotated_frame = result.plot()

        # 프레임 크기 조정 (1000x1000)
        annotated_frame = cv2.resize(annotated_frame, (1000, 1000))
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()

        # 프레임 전송
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()


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
