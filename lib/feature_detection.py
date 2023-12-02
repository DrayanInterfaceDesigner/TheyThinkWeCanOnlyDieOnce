import dlib
import cv2
import configparser
import numpy as np


class FeatureDetection:
    def __init__(self, configuration_filepath: str = None):
        self.configuration = self.config(configuration_filepath)
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.configuration["shape_predictor_path"])
        

    def config(self, configuration_filepath: str) -> dict:
        parser = configparser.ConfigParser()
        parser.read(configuration_filepath)

        clahe_tile_grid_size = parser.get("Detection", "clahe_tile_grid_size").split(",")
        clahe_tile_grid_size = tuple(map(int, clahe_tile_grid_size))
        return {
            "clahe_enhancement": parser.getboolean("Detection", "clahe_enhancement"),
            "clahe_clip_limit": parser.getfloat("Detection", "clahe_clip_limit"),
            "clahe_tile_grid_size": clahe_tile_grid_size,
            "contrast_increase": parser.getfloat("Detection", "contrast_increase"),
            "brightness_increase": parser.getfloat("Detection", "brightness_increase"),
            "histogram_equalization": parser.getboolean("Detection", "histogram_equalization"),
            "shape_predictor_path": parser.get("Detection", "shape_predictor_path"),
            "crisp_enhancement": parser.getboolean("Detection", "crisp_enhancement"),
            "stabelize_landmarks": parser.getboolean("Detection", "stabelize_landmarks"),
            "draw_landmarks": parser.getboolean("Detection", "draw_landmarks"),
        }
    
    def crisp_enhancement_pipeline(self, frame):
        kernel = np.array([
            [-1, -1, -1],
            [-1, 9, -1],
            [-1, -1, -1]
        ])
        return cv2.filter2D(frame, -1, kernel)

    def image_to_gray_pipeline(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    def histogram_equalization_pipeline(self, frame_gray):
        return cv2.equalizeHist(frame_gray)
    
    def brightness_increase_pipeline(self, frame_gray):
        return cv2.add(frame_gray, self.configuration["brightness_increase"])
    
    def contrast_increase_pipeline(self, frame_gray):
        return cv2.multiply(frame_gray, self.configuration["contrast_increase"])
    
    def clahe_enhancement_pipeline(self, frame_gray):
        clahe = cv2.createCLAHE(
            clipLimit=self.configuration["clahe_clip_limit"],
            tileGridSize=self.configuration["clahe_tile_grid_size"]
        )
        return clahe.apply(frame_gray)
    
    def get_closes_face(self, faces):
        if len(faces) == 0:
            return None
        else:
            return faces[0]
        
    def halve_landmark(self, landmark) -> tuple:
        return ((landmark[0][0] + landmark[1][0]) // 2, (landmark[1][1] + landmark[1][1]) // 2)

    # need to test if they're composed
    # and set a threshold for the distance between the last detected landmark and the current one
    # if the distance is too small, we don't update the landmark
    # if the distance is just enough, we update the landmark to a interpolation between the 
    # last and the current one.
    # if the distance is too big, we update the landmark to the current one.    
    # def stabelize_landmarks(self, landmarks):
    #     for key in landmarks.keys():
    #         landmarks[key] = tuple(map(int, landmarks[key]))
    
    def detect(self, frame) -> (dict | None):

        _frame = self.image_to_gray_pipeline(frame)
        _frame = self.brightness_increase_pipeline(_frame)
        # _frame = self.contrast_increase_pipeline(_frame)

        if self.configuration["crisp_enhancement"]:
            _frame = self.crisp_enhancement_pipeline(_frame)

        if self.configuration["histogram_equalization"]:
            _frame = self.histogram_equalization_pipeline(_frame)
        
        if self.configuration["clahe_enhancement"]:
            _frame = self.clahe_enhancement_pipeline(_frame)

        faces = self.detector(_frame, 1)
        # print(len(faces), faces)
        face = self.get_closes_face(faces)

        if face is None:
            return None
        else:
            landmarks = self.predictor(_frame, face)
            left_eye = [(landmarks.part(0).x, landmarks.part(0).y), (landmarks.part(1).x, landmarks.part(1).y)]
            right_eye = [(landmarks.part(2).x, landmarks.part(2).y), (landmarks.part(3).x, landmarks.part(3).y)]
            nose_tip = (landmarks.part(4).x, landmarks.part(4).y)
            
            left_eye_center = self.halve_landmark(left_eye)
            right_eye_center = self.halve_landmark(right_eye)

            if self.configuration["draw_landmarks"]:
                cv2.circle(frame, nose_tip, 3, (0, 255, 0), -1)
                cv2.circle(frame, left_eye_center, 3, (255, 0, 255), -1)
                cv2.circle(frame, right_eye_center, 3, (255, 0, 255), -1)
                # for landmark in landmarks.parts():
                #     cv2.circle(frame, (landmark.x, landmark.y), 3, (0, 255, 0), -1)

                cv2.circle(_frame, nose_tip, 3, (0, 255, 0), -1)
                cv2.circle(_frame, left_eye_center, 3, (255, 0, 255), -1)
                cv2.circle(_frame, right_eye_center, 3, (255, 0, 255), -1)

            landmarks = {
                "left_eye": left_eye,
                "right_eye": right_eye,
                "nose_tip": nose_tip,
                "left_eye_center": left_eye_center,
                "right_eye_center": right_eye_center,
                "frame": frame,
                "detection_frame": _frame,
            }
            return landmarks
