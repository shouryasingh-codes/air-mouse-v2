# 🧠 AI Air Mouse Controller — Lucky V2.2

This project lets you control your computer mouse using hand gestures through a webcam.  
No external sensors, just Python + your webcam doing the magic 😎  

I built this step by step to understand how real-time hand tracking, gesture detection, and smooth cursor movement work — not just to make it run, but to learn the logic behind every action.

---

## 🎯 What It Can Do
- 🖱️ **Single & Double Click** — pinch your thumb and index finger  
- ✋ **Drag & Drop** — hold the pinch longer  
- 🖐️ **Scroll Up / Down** — pinch thumb + middle finger and move your hand  
- 👉 **Right Click** — bring pinky close to thumb  
- 🎯 **Smooth Cursor Movement** — adaptive smoothing for stable motion  

---

## ⚙️ Tech Used
- **Language:** Python  
- **Libraries:**  
  - OpenCV (camera and overlay)  
  - MediaPipe (hand tracking)  
  - PyAutoGUI (mouse control)  

---

## 🚀 How To Run
1. Install requirements:
   ```bash
   pip install opencv-python mediapipe pyautogui    
python main.py

## 🧩 How It Works
MediaPipe tracks your hand landmarks in real-time.  
Distances between fingers decide which gesture is active,  
and PyAutoGUI performs that mouse action.  
A smoothing algorithm keeps cursor motion natural.

## 💡 Why I Made This
I built this to learn real-time tracking and computer vision.  
It’s simple, fun, and helped me understand gesture logic deeply.

## 👤 Author
**Shourya Singh**  
Built step by step (Day 1 → Day 6) to learn, test ideas, and improve logic.  
Next goal: make more AI-powered projects 🚀


