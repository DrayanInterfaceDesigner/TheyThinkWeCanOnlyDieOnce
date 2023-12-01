import face_recognition
import cv2

# Function to detect facial landmarks in real-time using the webcam
def detect_landmarks_webcam():
    # Open a connection to the webcam (you can change the index if you have multiple cameras)
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        # Find all face landmarks in the frame
        face_landmarks_list = face_recognition.face_landmarks(frame)

        if face_landmarks_list:
            # Extract landmarks for eyes and nose
            for landmarks in face_landmarks_list:
                # Print landmarks for eyes
                print("Eyes Landmarks:")
                for point in landmarks['left_eye'] + landmarks['right_eye']:
                    print(f"Point: {point}")

                # Print landmarks for nose (adjust as needed)
                print("Nose Landmarks:")
                for point in landmarks['nose_bridge'] + landmarks['nose_tip']:
                    print(f"Point: {point}")

            # Display the frame with landmarks (optional)
            for face_landmarks in face_landmarks_list:
                for facial_feature in face_landmarks.keys():
                    for point in face_landmarks[facial_feature]:
                        cv2.circle(frame, point, 2, (0, 255, 0), -1)

        # Display the frame
        cv2.imshow("Facial Landmarks", frame)

        # Break the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()

# Call the function to start webcam facial landmarks detection
detect_landmarks_webcam()
