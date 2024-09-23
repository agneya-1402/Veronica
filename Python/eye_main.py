import cv2
import numpy as np
import serial
import time

# Initialize the webcam
cap = cv2.VideoCapture(1)

# Initialize serial communication with Arduino
arduino = serial.Serial('/dev/cu.usbmodem1101', 9600, timeout=1)
time.sleep(2)  # Allow time for connection to establish

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - out_min) + out_min

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces with higher confidence by tweaking scaleFactor and minNeighbors
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=6)

    if len(faces) > 0:
        # Only process the first detected face
        (x, y, w, h) = faces[0]

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Calculate center of the face
        center_x = x + w // 2
        center_y = y + h // 2

        # Map face coordinates to servo angles (0-180)
        servo_x = map_range(center_x, 0, frame.shape[1], 0, 180)
        servo_y = map_range(center_y, 0, frame.shape[0], 0, 180)

        # Send coordinates to Arduino
        arduino.write(f"{servo_x},{servo_y}\n".encode())

    cv2.imshow('Face Detection', frame)

    # Exit on 'Esc' key
    if cv2.waitKey(1) & 0xFF == 27:  # 27 is the ASCII code for the Esc key
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
