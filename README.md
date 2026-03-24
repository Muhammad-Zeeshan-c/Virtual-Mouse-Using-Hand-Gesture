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

### ⚡ One-Click Launch (Recommended)
Just double-click **`start.bat`** — it will:
1. Check that Python and npm are installed.
2. Auto-download the hand tracking model if missing.
3. Install frontend dependencies if needed.
4. Launch both Backend and Frontend in separate terminals.

### Method B: Run Manually
1. **Start the Frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
2. **Start the Backend** (in a new terminal):
   ```bash
   cd src
   python main.py
   ```
3. Open `http://localhost:5173` for the dashboard.

### Method C: Backend Only
```bash
cd src
python main.py
```

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
├── start.bat              # One-click launcher
├── README.md
├── requirements.txt
├── .gitignore
├── documentation/
│   └── student_manual.md  # Educational walkthrough
├── src/
│   ├── main.py            # Entry point & Execution loop
│   ├── hand_tracker.py    # MediaPipe landmark detection
│   ├── gesture_logic.py   # Gesture recognition engine
│   ├── mouse_controller.py# Cursor control + smoothing
│   └── server.py          # FastAPI WebSocket server
├── frontend/
│   ├── src/
│   │   ├── App.jsx        # Dashboard UI
│   │   └── index.css      # Tailwind V4 styles
│   └── ...
└── ...
```

---
*Developed as a premium AI interaction project.*
