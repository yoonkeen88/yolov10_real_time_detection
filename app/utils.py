# import os
# import time
# import cv2
# import numpy as np
# from ultralytics import YOLO
# # from routes import socketio

# # YOLO 모델 로드
# model = YOLO('best.pt')

# # "drowsy" 감지 시간 저장을 위한 리스트를 모듈 수준에서 선언
# drowsy_detections = []

# def gen_frames():
#     cap = cv2.VideoCapture(0)  # 웹캠 사용 (0번 카메라)
#     if not cap.isOpened():
#         print("Error: Could not open webcam.")
#         return

#     while True:
#         success, frame = cap.read()
#         if not success:
#             break

#         results = model(frame)

#         # 현재 시간
#         current_time = time.time()

#         for result in results:
#             for box in result.boxes:
#                 # 클래스 이름과 확률을 추출
#                 class_name = result.names[int(box.cls)]
#                 confidence = box.conf
#                 label = f"{class_name} {confidence:.2f}"

#                 # "Drowsy"가 감지되었는지 확인
#                 if "Drowsy" in label:
#                     drowsy_detections.append(current_time)
#                     # 10초가 지난 감지 시간은 리스트에서 제거
#                     drowsy_detections[:] = [t for t in drowsy_detections if current_time - t <= 10]
#                     # Drowsy 감지 시 클라이언트에 알림
#                     socketio.emit('drowsy_detected', {'warning': True})
#                     break

#             annotated_frame = result.plot()

#         # 프레임 크기 조정 (1000x1000)
#         annotated_frame = cv2.resize(annotated_frame, (1000, 1000))
#         ret, buffer = cv2.imencode('.jpg', annotated_frame)
#         frame = buffer.tobytes()

#         # 프레임 전송
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#     cap.release()

# def process_video(filepath):
#     # Create output file path
#     output_filepath = os.path.splitext(filepath)[0] + '_processed.mp4'
    
#     # Open video file
#     cap = cv2.VideoCapture(filepath)
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter(output_filepath, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         results = model(frame)
#         annotated_frame = results.render()[0]
#         out.write(annotated_frame)

#     cap.release()
#     out.release()
#     return output_filepath
