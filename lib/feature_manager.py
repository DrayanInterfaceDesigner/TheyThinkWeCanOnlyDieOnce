class FeatureManager:
    def __init__(self) -> None:
        self.features: list = []
        self.features_map: dict = {}

    def add_feature(self, feature: object) -> None:
        _feature = {
            'id': len(self.features) + 1,
            'name': feature.label,
            'feature': feature
        }
        self.features.append(_feature)
        self.features_map[_feature['name']] = _feature
    
    def remove_feature(self, name: str) -> None:
        _feature = self.get_feature(name)
        self.features.remove(_feature)
        del self.features_map[name]
    
    def get_feature(self, name: str) -> object:
        return self.features_map[name]
    
    def get_features(self) -> list:
        return self.features
    
    def update(self, delta: float) -> None:
        for feature in self.features:
            feature['feature'].update(delta)

    def render(self, screen) -> None:
        for feature in self.features:
            feature['feature'].render(screen)
    

    
