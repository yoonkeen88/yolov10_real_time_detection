from flask import Blueprint, render_template, Response, request, redirect, url_for, send_file, current_app, jsonify
from werkzeug.utils import secure_filename
import os
from .utils import gen_frames, process_video  

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/webcam')
def webcam():
    return render_template('webcam.html')

@main.route('/check_drowsy')
def check_drowsy():
    global drowsy_detections
    if len(drowsy_detections) >= 5:  # 경고를 위한 임계값 설정 (예: 5회)
        return jsonify({"warning": True})
    return jsonify({"warning": False})

@main.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
