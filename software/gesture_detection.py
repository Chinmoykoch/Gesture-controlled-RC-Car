import cv2
import mediapipe as mp
import numpy as np
import requests
import time
# Replace with your ESP32's IP address
ESP32_IP = ""  # Example IP, change to actual
# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)
finger_tips = [4, 8, 12, 16, 20]
finger_base = [2, 5, 9, 13, 17]
def fingers_up(hand_landmarks):
    fingers = []
    if hand_landmarks.landmark[finger_tips[0]].x > hand_landmarks.landmark[finger_base[0]].x:
        fingers.append(1)
    else:
        fingers.append(0)
    for i in range(1, 5):
        if hand_landmarks.landmark[finger_tips[i]].y < hand_landmarks.landmark[finger_base[i]].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers
def get_gesture_command(fingers):
    if fingers == [1, 1, 1, 1, 1]: return 'F'
    elif fingers == [0, 1, 0, 0, 0]: return 'L'
    elif fingers == [0, 0, 0, 0, 1]: return 'R'
    elif fingers == [0, 1, 1, 1, 0]: return 'B'
    elif fingers == [0, 0, 0, 0, 0]: return 'S'
    return None
previous_command = None
try:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        current_command = None
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                fingers = fingers_up(hand_landmarks)
                current_command = get_gesture_command(fingers)
        if current_command and current_command != previous_command:
            try:
                url = f"{ESP32_IP}/cmd?move={current_command}"
                response = requests.get(url)
                if response.status_code == 200:
                    print(f"Sent command: {current_command}")
                    previous_command = current_command
                else:
                    print("Failed to send command")
            except Exception as e:
                print(f"HTTP error: {e}")
        cv2.putText(image, f'Command: {previous_command}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Gesture Control', image)
        time.sleep(0.1)
        if cv2.waitKey(5) & 0xFF == 27:
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Resources released")