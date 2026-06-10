# 📚 Smart Study Monitor

A Real-Time AI-Powered Posture & Distraction Monitoring System built to enhance focus, productivity, and digital well-being.

Smart Study Monitor uses Computer Vision and Machine Learning to track posture, detect distractions, and monitor user presence during study or work sessions.

---

## 🚀 Inspiration

With the rise of online learning, remote work, and digital classrooms, prolonged screen usage has led to:

- Poor posture ("Text Neck" syndrome)
- Increased mobile phone distractions
- Reduced productivity
- Lack of supervision in online environments

Smart Study Monitor is designed to address these modern digital challenges using real-time AI monitoring.

---

## 🎯 Features

### 1️⃣ Smart Calibration System
- 3-second automatic calibration phase at session start.
- Calculates baseline posture angle using:
  - Nose landmark
  - Shoulder landmark
  - Hip landmark
- Establishes personalized posture reference.

### 2️⃣ Real-Time Posture Tracking
- Continuously calculates body angle.
- Triggers alert if posture deviates more than **10° from baseline**.
- Helps prevent long-term spinal issues.

### 3️⃣ Distraction Detection (YOLOv8)
- Detects "cell phone" objects in real time.
- Triggers alert if phone usage is detected.
- Encourages distraction-free study sessions.

### 4️⃣ Absence Monitoring
- Detects if user leaves the seat.
- Flags absence longer than **3 seconds**.
- Useful for exam monitoring and productivity tracking.

### 5️⃣ Real-Time Video Streaming
- Uses WebSockets for live camera frame streaming.
- Instant UI updates in React frontend.

---

## 🏗️ System Architecture

```

PC Camera
↓
Python Flask Backend
↓
MediaPipe Pose + YOLOv8 Processing
↓
Flask-SocketIO (WebSockets)
↓
React Frontend (Live Updates + Animations)

````

---

## 🛠️ Tech Stack

### 🔹 Frontend
- React.js
- Framer Motion (Animations & UI transitions)

### 🔹 Backend
- Python Flask
- Flask-SocketIO (Real-time communication)

### 🔹 AI / ML
- MediaPipe Pose (Skeletal Tracking)
- YOLOv8 (Object Detection)

### 🔹 Communication
- WebSockets (Low-latency frame transmission)

---

## ⚙️ Installation & Setup

### 🔹 1. Clone the Repository

```bash
git clone https://github.com/your-username/Smart-Study-Monitor.git
cd Smart-Study-Monitor
````

---

### 🔹 2. Backend Setup (Flask)

```bash
cd backend
pip install -r requirements.txt
python app.py
```

---

### 🔹 3. Frontend Setup (React)

```bash
cd frontend
npm install
npm start
```

---

### 🔹 4. Run the Application

* Open browser at: `http://localhost:3000`
* Allow camera access
* Sit straight during calibration
* Start monitoring

---

## 📐 Core Logic Explanation

### 🧮 Posture Angle Calculation

The posture angle is computed using three key body landmarks:

* Nose
* Shoulder
* Hip

Using vector angle calculation:

```
Angle = arccos( (A·B) / (|A||B|) )
```

Where:

* A = Vector (Shoulder → Nose)
* B = Vector (Shoulder → Hip)

If deviation > 10° → Posture Alert Triggered.

---

## 🌍 Real-World Applications

* 👨‍🎓 Students during online classes
* 🧑‍💻 Remote employees
* 📝 Online exam monitoring systems
* 👨‍👩‍👧 Parents tracking children’s digital posture habits
* 🏢 Corporate productivity monitoring

---

## 🔐 Future Enhancements

* Session analytics dashboard
* Weekly posture improvement reports
* Cloud-based monitoring
* Multi-user support
* Mobile application version

---

## 📊 Project Highlights

* Real-time AI inference
* Low-latency WebSocket streaming
* Personalized posture baseline
* Hybrid AI system (Pose + Object Detection)
* Full-stack architecture

---

## 👨‍💻 Author

Developed as an AI-based productivity enhancement system integrating Computer Vision and Full-Stack technologies.

---

## 📜 License

This project is developed for educational and research purposes.

