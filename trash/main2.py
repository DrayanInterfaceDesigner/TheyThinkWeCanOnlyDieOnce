# Import necessary libraries
import dlib
import cv2
from multiprocessing.connection import Listener

# Establish a connection for inter-process communication
print("Waiting for connection in listener script...")
address = ('localhost', 6000)
listener = Listener(address, authkey=b'secret_key')
conn = listener.accept()
print('connection accepted from', listener.last_accepted)

# Histogram Constrast Equalization
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

def send_positions(connection, landmarks):
    connection.send(landmarks)

def increase_contrast(image, contrast_factor):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Increase the contrast by multiplying all pixel values with the contrast factor
    contrast_adjusted = cv2.multiply(gray, contrast_factor)

    # Convert back to the original image format (BGR)
    contrast_adjusted_bgr = cv2.cvtColor(contrast_adjusted, cv2.COLOR_GRAY2BGR)

    return contrast_adjusted_bgr


def increase_contrast_clahe(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply histogram contrast equalization
    contrast_adjusted = clahe.apply(gray)

    # Convert back to the original image format (BGR)
    contrast_adjusted_bgr = cv2.cvtColor(contrast_adjusted, cv2.COLOR_GRAY2BGR)

    return contrast_adjusted_bgr


# Load the pre-trained facial landmark detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to grayscale for facial landmark detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = detector(gray)

    for face in faces:
        # Get the facial landmarks for the current face
        landmarks = predictor(gray, face)

        # Draw circles around each facial landmark point
        eye_left = [(landmarks.part(0).x, landmarks.part(0).y), (landmarks.part(1).x, landmarks.part(1).y)]
        eye_right = [(landmarks.part(2).x, landmarks.part(2).y), (landmarks.part(3).x, landmarks.part(3).y)]

        mid_left_eye = ((eye_left[0][0] + eye_left[1][0]) // 2, (eye_left[0][1] + eye_left[1][1]) // 2)
        mid_right_eye = ((eye_right[0][0] + eye_right[1][0]) // 2, (eye_right[0][1] + eye_right[1][1]) // 2)
    
        nose_tip = (landmarks.part(4).x, landmarks.part(4).y)

        cv2.circle(frame, nose_tip, 3, (0, 255, 0), -1)
        cv2.circle(frame, mid_left_eye, 3, (255, 0, 255), -1)
        cv2.circle(frame, mid_right_eye, 3, (255, 0, 255), -1)

        # Send the landmarks positions to the other script
        send_positions(conn, [mid_left_eye, mid_right_eye, nose_tip])

    # Display the frame with facial landmarks
    cv2.imshow("Facial Landmarks", frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
