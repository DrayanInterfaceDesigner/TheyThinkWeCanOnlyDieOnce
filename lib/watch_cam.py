import cv2
import configparser
from lib import FeatureDetection

class WatchCam:
    def __init__(self, detection: FeatureDetection, configuration_filepath: str):
        self.configuration = self.config(configuration_filepath)
        self.capture = None
        self.is_capture_ok = False
        self.is_watching = False
        self.detection = detection
    
    def config(self, configuration_filepath: str) -> dict:
        parser = configparser.ConfigParser()
        parser.read(configuration_filepath)
        return {
            "camera": parser.get("Camera", "camera"),
            "camera_fps": parser.getfloat("Camera", "fps"),
            "image_flip": parser.getboolean("Camera", "image_flip"),
            "im_show": parser.getboolean("Camera", "show_capture"),
            "debug_mode": parser.getboolean("Debug", "debug_mode"),
        }
    
    def start_capture(self):
        if not self.is_watching:
            self.is_watching = True
            self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            # self.capture.set(cv2.CAP_PROP_FPS, self.configuration["camera_fps"])

    def start_to_watch(self):
        self.start_capture()
        while self.is_watching:
            self.is_capture_ok, frame = self.capture.read()

            if self.is_capture_ok:

                if self.configuration["image_flip"]:
                    frame = cv2.flip(frame, 1)  
                
                _detections = self.detection.detect(frame)
                
                if self.configuration["debug_mode"]:
                    if _detections is not None:
                        frame = _detections["frame"]

                if self.configuration["im_show"]:
                    cv2.imshow("frame", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.is_watching = False
                    break
        self.capture.release()
        cv2.destroyAllWindows()
        
        



