# 🤖 Gesture-Controlled Robot

This project allows you to control a robot car using hand gestures captured by a webcam. The system uses an ESP32 microcontroller for the robot and OpenCV with MediaPipe for hand gesture recognition.

## 📸 Project Images

### Robot Hardware
<img src="/images/hardware.jpeg" alt="Robot Front View" width="400"/>
*Front view of the assembled robot*

### Circuit Diagram
<img src="/images/circuit.png" alt="Hardware Circuit Diagram" width="400"/>
*Wiring diagram showing connections between ESP32, L298N driver, and motors*

### Gesture Detection
<img src="/images/gesture.png" alt="Hand Gesture Detection" width="400"/>
*Example of hand gesture detection with MediaPipe tracking*

## 📋 Table of Contents

- 🔌 Hardware Requirements
- 📊 Pin Connections
- 💻 Software Requirements
- 🛠️ Setup Instructions
- ▶️ Running the Project
- 👋 Gesture Controls 
- ⚠️ Troubleshooting
- 📝 Circuit Diagram

## 🔌 Hardware Requirements

- ESP32 development board
- L298N motor driver (or similar dual H-bridge motor driver)
- DC motors (2x)
- Robot chassis
- Jumper wires
- Power supply for motors (battery pack, recommended 6-12V)
- USB power bank (optional, for powering the ESP32)
- Laptop/computer with webcam

## 📊 Pin Connections

| ESP32 Pin | Connection |
|-----------|------------|
| GPIO 18   | ENA (Motor A Enable) |
| GPIO 19   | IN1 (Motor A Input 1) |
| GPIO 21   | IN2 (Motor A Input 2) |
| GPIO 5    | ENB (Motor B Enable) |
| GPIO 22   | IN3 (Motor B Input 1) |
| GPIO 23   | IN4 (Motor B Input 2) |

## 💻 Software Requirements

- Arduino IDE
- Python 3.x
- Required Python libraries:
  - OpenCV
  - MediaPipe
  - NumPy
  - Requests

## 🛠️ Setup Instructions

### Step 1: Hardware Assembly

1. Assemble the robot chassis according to its instructions
2. Mount the motors and connect them to the L298N motor driver
3. Connect the L298N motor driver to the ESP32 following the pin connections table above
4. Connect the power supply (battery) to the motor driver
   - Connect the positive terminal to the +12V (or VCC) on the motor driver
   - Connect the negative terminal to the GND on the motor driver
5. (Optional) Connect a USB power bank to the ESP32 for independent operation

### Step 2: ESP32 Setup

1. Install the Arduino IDE
2. Add ESP32 board support to Arduino IDE:
   - Go to File > Preferences
   - Add `https://dl.espressif.com/dl/package_esp32_index.json` to Additional Boards Manager URLs
   - Go to Tools > Board > Boards Manager
   - Search for "ESP32" and install
3. Install required libraries:
   - Go to Sketch > Include Library > Manage Libraries
   - Install "WiFi" and "WebServer" libraries
4. Update the WiFi credentials in the Arduino code:
   ```cpp
   const char* ssid = "Your_WiFi_SSID";
   const char* password = "Your_WiFi_Password";
   ```
5. Upload the Arduino code to your ESP32
6. Open Serial Monitor at 115200 baud to see the IP address assigned to ESP32
7. Note down this IP address for the Python script

### Step 3: Python Setup

1. Install the required Python libraries:
   ```bash
   pip install opencv-python mediapipe numpy requests
   ```
2. Update the ESP32 IP address in the Python script:
   ```python
   ESP32_IP = "http://192.168.X.X"  # Replace with your ESP32's IP address
   ```
3. Make sure your webcam is connected and operational

## ▶️ Running the Project

1. Power on the robot:
   - Connect the battery to the motor driver
   - Power the ESP32 (via USB or power bank)
2. Wait for the ESP32 to connect to WiFi (check Serial Monitor)
3. Run the Python script on your computer:
   ```bash
   python gesture_control.py
   ```
4. A window showing your webcam feed will open
5. Use hand gestures to control the robot

## 👋 Gesture Controls

| Gesture | Command | Robot Action |
|---------|---------|--------------|
| ✋ All fingers up (open hand) | F | Move Forward |
| ☝️ Index finger up | L | Turn Left |
| 🤙 Pinky finger up | R | Turn Right |
| 🖖 Middle three fingers up | B | Move Backward |
| ✊ All fingers down (closed fist) | S | Stop |

## ⚠️ Troubleshooting

- **Robot not responding to commands:**
  - Verify ESP32 is connected to WiFi (check Serial Monitor)
  - Confirm the correct IP address is set in the Python script
  - Check all physical connections
  - Ensure the battery has sufficient charge

- **Hand gestures not recognized:**
  - Ensure good lighting in the room
  - Keep your hand within the camera frame
  - Make clear, distinct gestures
  - Try adjusting the hand detection confidence in the MediaPipe setup

- **Motors not moving:**
  - Check motor connections
  - Verify battery voltage is sufficient
  - Ensure motor driver is receiving power

## 📝 Circuit Diagram

```
+--------+    +--------+    +----------+
| Battery |--->| L298N  |--->| Motors  |
+--------+    +--------+    +----------+
                  ^
                  |
              +--------+
              | ESP32  |
              +--------+
                  ^
                  |
      WiFi       |
    <----------->+
        ^
        |
  +-------------+
  | Computer    |
  | (webcam +   |
  |  Python)    |
  +-------------+
```

## 📌 Notes

- The ESP32 creates a web server that listens for commands
- The Python script uses computer vision to recognize hand gestures
- Commands are sent from the computer to the ESP32 via HTTP requests
- Ensure both the computer and ESP32 are on the same WiFi network

