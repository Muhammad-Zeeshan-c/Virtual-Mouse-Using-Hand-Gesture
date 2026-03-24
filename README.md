# AI Virtual Mouse using Hand Gesture Recognition

A real-time, AI-powered virtual mouse system that allows you to control your computer cursor using hand gestures. This project features a modular Python backend powered by MediaPipe and a modern React + TailwindCSS V4 dashboard for configuration and performance monitoring.

## 🚀 Features

- **Real-time Tracking:** 21 hand landmarks detected with MediaPipe.
- **Gesture Controls:**
  - `MOVE`: Pinch Index & Thumb and move hand.
  - `LEFT CLICK`: Quick tap Index & Thumb.
  - `RIGHT CLICK`: Touch Thumb & Middle finger.
  - `DRAG & DROP`: Close hand into a fist.
  - `SCROLL`: Touch Thumb & Pinky (move hand up/down).
- **Modern Dashboard:** Built with React & Tailwind V4 to adjust sensitivity and toggle features.
- **Anti-Jitter:** Smooth cursor movement using interpolation and weighted averages.

## 🛠️ Tech Stack

- **Backend:** Python, OpenCV, MediaPipe, PyAutoGUI, FastAPI.
- **Frontend:** React, TailwindCSS V4, Vite, Lucide Icons.

## 📥 Prerequisite

- Python 3.8+
- Node.js & npm (for the GUI)
- Webcam

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
cd AI-Virtual-Mouse
```

### 2. Backend Setup
```bash
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

## 🏃 How to Run

### Method A: Run with GUI (Recommended)
1. **Start the Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```
2. **Start the Backend:**
   In a new terminal:
   ```bash
   cd src
   python main.py
   ```
3. Open the link displayed in the frontend terminal (usually `http://localhost:5173`) to access the dashboard.

### Method B: Run Backend Only
If you don't need the GUI, you can just run:
```bash
cd src
python main.py
```
The system will use default settings.

## 🖱️ Hand Gestures Guide

| Action | Gesture |
| :--- | :--- |
| **Move Cursor** | Pinch Index & Thumb (hold and move) |
| **Left Click** | Quick tap Index & Thumb (pinch & release) |
| **Right Click** | Touch Thumb & Middle finger |
| **Scroll** | Touch Thumb & Pinky (move up/down) |
| **Drag & Drop** | Close hand into a fist |

## 📁 Project Structure

```
AI-Virtual-Mouse/
├── src/
│   ├── main.py            # Entry point & Execution loop
│   ├── hand_tracker.py    # Landmark detection
│   ├── gesture_logic.py   # Mapping logic
│   ├── mouse_controller.py# System mouse control
│   └── server.py          # FastAPI communication layer
├── frontend/              # React Dashboard
│   ├── src/
│   │   ├── App.jsx        # Dashboard UI
│   │   └── index.css      # Tailwind V4 styles
│   └── ...
├── requirements.txt       # Python dependencies
└── README.md              # Documentation
```

---
*Developed as a premium AI interaction project.*
