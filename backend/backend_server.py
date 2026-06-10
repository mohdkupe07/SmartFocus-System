import cv2
import base64
import time
import math
import winsound
import mediapipe as mp
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from ultralytics import YOLO

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# --- CONFIGURATION & PATHS ---
PHONE_SOUND = r"E:\ML Course\study-monitor\phone_alert.wav"
POSTURE_SOUND = r"E:\ML Course\study-monitor\posture_alert.wav"

# --- MODELS ---
yolo_model = YOLO("yolov8n.pt")
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# --- STATE ---
monitoring_active = False
session_end_time = 0
calibrated = False
ref_angle = None
calib_start = None
last_seen = time.time()
previous_status = "Stopped"

def calculate_angle(nose, shoulder, hip):
    """Calculates posture angle using your original PyQt math"""
    return abs(math.degrees(
        math.atan2(hip.y - shoulder.y, hip.x - shoulder.x) -
        math.atan2(nose.y - shoulder.y, nose.x - shoulder.x)
    ))

def draw_styled_overlay(frame, text, color_bgr):
    """Replicates the UI from image_df03c0.jpg"""
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.1
    thickness = 3
    (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
    
    # Semi-transparent dark background box
    overlay = frame.copy()
    cv2.rectangle(overlay, (20, 20), (text_w + 50, text_h + 50), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    
    # Matching border and text color from your palette
    cv2.rectangle(frame, (20, 20), (text_w + 50, text_h + 50), color_bgr, 2)
    cv2.putText(frame, text, (35, text_h + 35), font, font_scale, color_bgr, thickness, cv2.LINE_AA)

def process_video():
    global monitoring_active, session_end_time, calibrated, ref_angle, calib_start, last_seen, previous_status
    cap = cv2.VideoCapture(1)
    
    while monitoring_active:
        ret, frame = cap.read()
        if not ret: break

        current_time = time.time()
        status_text = "Stopped"
        # BGR conversion of #7F9C96 (Cambridge Blue)
        status_color = (150, 156, 127) 

        # YOLO & MediaPipe Logic
        yolo_results = yolo_model(frame, verbose=False, conf=0.4)[0]
        phone_detected = any(int(box.cls[0]) == 67 for box in yolo_results.boxes)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            last_seen = current_time
            lm = results.pose_landmarks.landmark
            angle = calculate_angle(lm[0], lm[11], lm[23])

            if not calibrated:
                if calib_start is None: calib_start = current_time
                elif current_time - calib_start >= 3:
                    ref_angle, calibrated = angle, True
                status_text, status_color = "Calibrating", (121, 64, 27) # BGR for #1B4079
            else:
                if phone_detected:
                    status_text, status_color = "Phone Distraction", (138, 113, 248) # BGR for #F87171
                elif abs(angle - ref_angle) < 10:
                    status_text, status_color = "Correct Posture", (144, 223, 203) # BGR for #CBDF90
                else:
                    status_text, status_color = "Incorrect Posture", (138, 113, 248) # BGR for #F87171
        else:
            if current_time - last_seen > 3:
                status_text, status_color = "Student Left Seat", (138, 113, 248)

        # Trigger Audio only on status change
        if status_text != previous_status:
            if status_text == "Phone Distraction":
                winsound.PlaySound(PHONE_SOUND, winsound.SND_FILENAME | winsound.SND_ASYNC)
            elif status_text in ["Incorrect Posture", "Student Left Seat"]:
                winsound.PlaySound(POSTURE_SOUND, winsound.SND_FILENAME | winsound.SND_ASYNC)
            previous_status = status_text

        draw_styled_overlay(frame, status_text, status_color)
        
        remaining = int(session_end_time - current_time)
        _, buffer = cv2.imencode('.jpg', frame)
        frame_encoded = base64.b64encode(buffer).decode('utf-8')
        socketio.emit('status', {'status': status_text, 'timeLeft': max(0, remaining), 'frame': frame_encoded})
        socketio.sleep(0.03)

    cap.release()

@app.route('/start', methods=['POST'])
def start():
    global monitoring_active, session_end_time, calibrated, calib_start, ref_angle, last_seen, previous_status
    duration = float(request.json.get('duration', 25))
    session_end_time = time.time() + (duration * 60)
    monitoring_active, calibrated, calib_start, ref_angle, last_seen, previous_status = True, False, None, None, time.time(), "Stopped"
    socketio.start_background_task(process_video)
    return jsonify({"status": "ok"})

@app.route('/stop', methods=['POST'])
def stop():
    global monitoring_active
    monitoring_active = False
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    socketio.run(app, port=5000, debug=False)