# 🚀 Smart Study Monitor: Quick Start Guide

This guide will help you get your AI-powered study environment up and running in minutes using your PC's integrated camera.

---

## 📂 1. Project Organization
Ensure your folders are structured like this:
- `backend/`: Contains `backend_server.py`, `yolov8n.pt`, and `.wav` alert files.
- `frontend/`: Contains your React project files (using `npm start`).

---

## ⚙️ 2. Backend Setup (Flask + AI)
Open a terminal, navigate to your `backend` folder, and run these commands:

1. **Create Virtual Environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate

```

2. **Install AI Libraries**:
*Note: We use MediaPipe 0.10.11 for maximum stability with the Pose solutions API.*
```bash
pip install flask flask-socketio flask-cors opencv-python ultralytics mediapipe==0.10.11

```


3. **Launch Server**:
```bash
python backend_server.py

```


*Keep this terminal open. It will print "AI Models Ready" once initialized.*

---

## 💻 3. Frontend Setup (React Dashboard)

Open a **new** terminal, navigate to your `frontend` folder, and run these commands:

1. **Install UI Packages**:
```bash
npm install socket.io-client framer-motion

```


2. **Launch Dashboard**:
```bash
npm start

```


*The app will automatically open at `http://localhost:3000`.*

---

## 🧪 4. Running the Demo Session

1. **Set Duration**: Enter your study time (e.g., 25 minutes) in the sidebar.
2. **Start**: Click the **"Start Study"** button.
3. **Calibrate**: Sit in your **ideal upright posture** for the first 3 seconds. The AI maps your nose, shoulders, and hips to set your baseline.
4. **Test Features**:
* **Posture**: Slouch forward to see the "Incorrect Posture" alert.
* **Distraction**: Hold up a phone to trigger the YOLOv8 detection.
* **Absence**: Step out of the camera's view for 3 seconds.



---

## 🛠️ Troubleshooting

* **Failed to Fetch**: Ensure the Backend terminal is still running on port 5000.
* **Camera Not Found**: Close other apps (like Zoom) that might be using the webcam.
* **Dependency Error**: If MediaPipe fails to load, ensure you are using the version `0.10.11` as specified.

```

---

