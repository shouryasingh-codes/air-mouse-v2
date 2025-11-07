# -------------------------------------------------------------
# Project : AI Air Mouse Controller
# Author  : Lucky Singh
# Date    : November 2025
# About   : A simple project that lets you control the mouse 
#           using hand gestures through a webcam.
#           Supports single click, double click, scroll, and 
#           right-click gestures with smooth movement and visual feedback.
# Note    : Built step by step (Day 1 to Day 6) to practice logic,
#           structure, and gesture-based control with python.
# -------------------------------------------------------------
 
# Force update to refresh GitHub sync

import cv2
import mediapipe as mp
import pyautogui as pg
import math
import time
from collections import deque

# Webcam & screen setup
cap = cv2.VideoCapture(0)
screen_w, screen_h = pg.size()

# MediaPipe setup
mp_hand = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# State variables
scrol_pinch = 0.08
distance_click = 0.05
last_positions = deque(maxlen=5)
pinch_active = False
dragging = False
last_click_time = 0
double_click_threshold = 0.3
last_right_t = 0


def get_smooth_position(new_x, new_y):
    """
    Keeps the cursor movement smooth by averaging the last few positions.
    This reduces sudden jumps in cursor movement when hand speed changes.
    """
    last_positions.append((new_x, new_y))
    avg_x = sum(x for x, _ in last_positions) / len(last_positions)
    avg_y = sum(y for _, y in last_positions) / len(last_positions)
    return int(avg_x), int(avg_y)


def pinch_double_click(index_tip, thumb_tip, frame):
    """
    Handles single and double click gestures based on the distance between
    the thumb and index finger. Also manages drag start and end.
    """
    global pinch_active, dragging, last_click_time
    dist = math.hypot(index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y)

    if dist < distance_click:
        current_time = time.time()
        if not pinch_active:
            if current_time - last_click_time < double_click_threshold:
                pg.doubleClick()
                cv2.putText(frame, "🖱️ Double Click", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                pg.click()
                cv2.putText(frame, "✅ Single Click", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            pinch_active = True
            dragging = True
            pg.mouseDown()
            last_click_time = current_time
    else:
        if dragging:
            pg.mouseUp()
            dragging = False
            pinch_active = False
            cv2.putText(frame, "🛑 Drag End", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


def Hand_scroll(middle_tip, thumb_tip, index_tip, frame):
    """
    Detects thumb–middle finger pinch for scrolling.
    If the index finger moves up or down, it scrolls accordingly.
    """
    scrol = math.hypot(middle_tip.x - thumb_tip.x, middle_tip.y - thumb_tip.y)

    if scrol < scrol_pinch:
        if index_tip.y < 0.4:
            pg.scroll(50)
            cv2.putText(frame, "⬆️ Scrolling Up", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif index_tip.y > 0.6:
            pg.scroll(-50)
            cv2.putText(frame, "⬇️ Scrolling Down", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)


def right_click(pinky_tip, thumb_tip, frame):
    """
    Detects right-click gesture using pinky and thumb distance.
    Performs a right-click when the fingers come close briefly.
    """
    global last_right_t

    right_click_dist = math.hypot(pinky_tip.x - thumb_tip.x, pinky_tip.y - thumb_tip.y)
    right_click_t = time.time()

    if right_click_dist < 0.05:
        if right_click_t - last_right_t > 0.03:
            pg.rightClick()
            cv2.putText(frame, "👉 Right Click", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        last_right_t = right_click_t


def hand_gesture(frame):
    """
    Processes each frame:
      - Detects hand landmarks using MediaPipe.
      - Moves the cursor smoothly.
      - Calls gesture functions (click, scroll, right-click).
    """
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hand.HAND_CONNECTIONS)

            pinky_tip = hand_landmarks.landmark[mp_hand.HandLandmark.PINKY_TIP]
            index_tip = hand_landmarks.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = hand_landmarks.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hand.HandLandmark.THUMB_TIP]

            # Map hand position to screen
            target_x = int(index_tip.x * screen_w)
            target_y = int(index_tip.y * screen_h)

            curr_x, curr_y = pg.position()
            distance = math.hypot(curr_x - target_x, curr_y - target_y)
            speed = distance / 0.033

            # Adaptive smooth factor
            if speed < 3:
                smooth_factor = 0
            elif speed < 5:
                smooth_factor = 0.05
            elif speed < 50:
                smooth_factor = 0.2
            else:
                smooth_factor = 0.5

            new_x = curr_x + (target_x - curr_x) * smooth_factor
            new_y = curr_y + (target_y - curr_y) * smooth_factor

            smooth_x, smooth_y = get_smooth_position(new_x, new_y)
            pg.moveTo(smooth_x, smooth_y, duration=0.01)

            # Gesture checks
            pinch_double_click(index_tip, thumb_tip, frame)
            Hand_scroll(middle_tip, thumb_tip, index_tip, frame)
            right_click(pinky_tip, thumb_tip, frame)

    return frame


hands = mp_hand.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.5)

while True:
    ret, frame = cap.read()
    frame = hand_gesture(frame)
    cv2.imshow("AI Air Mouse Controller - Lucky V2.2", frame)

    if cv2.waitKey(1) & 0xFF == ord('d'):
        break

cap.release()
cv2.destroyAllWindows()
