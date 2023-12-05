from .feature_detection import FeatureDetection as FeatureDetection
from .feature_manager import FeatureManager as FeatureManager
from .feature import Feature as Feature
from .sprite import Sprite as Sprite
from .vector2 import Vector2 as Vector2
from utils import type_infer
import configparser

class BuildFace:
    def __init__(self, feature_manager: FeatureManager, detection: FeatureDetection, configuration_filepath: str) -> None:
        self.FM = feature_manager
        self.path: str = configuration_filepath
        self.configuration: dict = self.config(configuration_filepath)
        self.detection: FeatureDetection = detection
        self.features_names: list = []
        self.features: list = []
        self.config(configuration_filepath)
        self.build_features()

    def config(self, configuration_filepath: str) -> dict:
        parser = configparser.ConfigParser()
        parser.read(configuration_filepath)

        self.features_names = parser.sections()
    
        _config = {}
        for feature in self.features_names:
            # print(feature)
            _ = {}
            for key, value in parser.items(feature):
                _[key] = type_infer.convert_to_proper_type(value)
            _config[feature] = _
        
        self.features_names.remove("General")
        self.features = _config
        return _config
    
    def build_features(self):
        for name in self.features_names:
            feature = self.features[name]
            fpath = self.path.split(".config")[0] + "assets/" + feature['fname'] 
            sprite = Sprite(fpath, Vector2(), feature['width'], feature['height'])
            Feature(self.FM, sprite, self.detection, feature['point_name'], feature)


    