import cv2
import mediapipe as mp
import pyautogui as pg
import math
import time
from collections import deque

# Webcam & screen setup
cap = cv2.VideoCapture(0)
screen_w, screen_h = pg.size()

# MediaPipe hands
mp_hand = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# State variables
smooth_factor = 0.2
distance_click = 0.05
last_positions = deque(maxlen=5)
pinch_active = False
dragging = False

# Double-click detection
last_click_time = 0
double_click_threshold = 0.3  # seconds between two pinches

def get_smooth_position(new_x, new_y):
    last_positions.append((new_x, new_y))
    avg_x = sum(x for x,_ in last_positions) / len(last_positions)
    avg_y = sum(y for _,y in last_positions) / len(last_positions)
    return int(avg_x), int(avg_y)

def hand_gesture(frame):
    global pinch_active, dragging, last_click_time
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hand.HAND_CONNECTIONS)

            # Landmarks
            index_tip = hand_landmarks.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hand.HandLandmark.THUMB_TIP]

            # Screen coordinates
            target_x = int(index_tip.x * screen_w)
            target_y = int(index_tip.y * screen_h)

            # Linear interpolation
            curr_x, curr_y = pg.position()
            new_x = curr_x + (target_x - curr_x) * smooth_factor
            new_y = curr_y + (target_y - curr_y) * smooth_factor

            # Moving average
            smooth_x, smooth_y = get_smooth_position(new_x, new_y)

            # Pinch distance
            dist = math.hypot(index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y)

            # ✨ Gesture logic ✨
            if dist < distance_click:
                current_time = time.time()

                if not pinch_active:
                    # Check for double click
                    if current_time - last_click_time < double_click_threshold:
                        pg.doubleClick()
                        print("🖱️ Double Click!")
                    else:
                        pg.click()
                        print("✅ Single Click + Drag Start")

                    pinch_active = True
                    dragging = True
                    pg.mouseDown()  # start drag

                    last_click_time = current_time

            else:
                if dragging:
                    pg.mouseUp()
                    dragging = False
                    print("🛑 Drag End")
                    pinch_active = False

            # Cursor move
            pg.moveTo(smooth_x, smooth_y, duration=0.01)

    return frame

with mp_hand.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.5) as hands:
    while True:
        ret, frame = cap.read()
        frame = hand_gesture(frame)
        cv2.imshow("Lucky V2.1 - Air Mouse (Double Click Added)", frame)

        if cv2.waitKey(1) & 0xFF == ord('d'):
            break

cap.release()
cv2.destroyAllWindows()
