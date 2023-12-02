from lib import FeatureDetection
from utils import type_infer
import configparser

class DrawFace:
    def __init__(self, detection: FeatureDetection, configuration_filepath: str) -> None:
        self.configuration: dict = self.config(configuration_filepath)
        self.detection: FeatureDetection = detection
        self.features_names: list = []

    def config(self, configuration_filepath: str) -> dict:
        parser = configparser.ConfigParser()
        parser.read(configuration_filepath)

        self.features_names = parser.sections()
        _config = {}
        for feature in self.features_names:
            _ = {}
            for key, value in parser.items(feature):
                _[key] = type_infer(value)
            _config[feature] = _
        
        return _config
    
    def build_features(self):
        pass


    