import cv2
import mediapipe as mp
import serial
import time
# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Initialize the webcam
cap = cv2.VideoCapture(1)

# Initialize serial communication with Arduino
arduino = serial.Serial('/dev/cu.usbmodem1101', 9600, timeout=1)
time.sleep(2)  # Allow time for connection to establish

def amplified_map_range(x, in_min, in_max, out_min, out_max, amplification=1.5):
    # Calculate the middle points
    in_mid = (in_min + in_max) / 2
    out_mid = (out_min + out_max) / 2
    
    # Amplify the distance from the middle
    amplified_x = in_mid + (x - in_mid) * amplification
    
    # Ensure the amplified value is within the input range
    amplified_x = max(in_min, min(amplified_x, in_max))
    
    # Map the amplified value to the output range
    return int((amplified_x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Smoothing factor for servo movement (0 < alpha < 1)
# Lower values create smoother but slower movement
alpha = 0.3

# Initialize last_angle
last_angle = 90  # Start at the middle position

with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Convert the BGR image to RGB and process it with MediaPipe Face Detection
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image)

        # Convert the image color back so it can be displayed
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.detections:
            # Only consider the first detected face
            detection = results.detections[0]
            
            # Get the bounding box of the face
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = image.shape
            x, y = int(bboxC.xmin * iw), int(bboxC.ymin * ih)
            w, h = int(bboxC.width * iw), int(bboxC.height * ih)
            
            # Calculate the center of the face
            center_x = x + w // 2
            
            # Map the x-coordinate to servo angle with amplification
            new_angle = amplified_map_range(center_x, 0, iw, 0, 180, amplification=1.5)
            
            # Apply smoothing
            smooth_angle = int(alpha * new_angle + (1 - alpha) * last_angle)
            last_angle = smooth_angle
            
            # Send the servo angle to Arduino
            arduino.write(f"{smooth_angle}\n".encode())
            
            # Draw the face detection annotations on the image
            mp_drawing.draw_detection(image, detection)
            
            # Display the servo angle on the image
            cv2.putText(image, f"Servo Angle: {smooth_angle}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            # If no face is detected, display a message
            cv2.putText(image, "No face detected", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display the resulting image
        cv2.imshow('MediaPipe Face Detection', image)
        if cv2.waitKey(5) & 0xFF == 27:  # Press 'ESC' to exit
            break

cap.release()
cv2.destroyAllWindows()
arduino.close()
