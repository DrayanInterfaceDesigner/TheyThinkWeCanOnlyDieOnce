from .vector2 import Vector2 as Vector2
from .maths import lerp as lerp
class Feature:
    def __init__(self, manager, sprite, predictor, label, feature) -> None:
        self.manager = manager
        self.sprite = sprite
        self.predictor = predictor
        self.label = label
        self.feature = feature
        self.position: Vector2 = Vector2()
        self.acceleration: Vector2 = Vector2()
        self.velocity: Vector2 = Vector2()
        self.anchor: Vector2 = Vector2()
        self.size: dict = {
            "width": 0.0,
            "height": 0.0
        }
        self.mass: float = 0.0
        self.radius: float = 0.0
        self.speed: float = 0.0
        self.max_speed: float = 0.0
        self.max_force: float = 0.0
        self.angle: float = 0.0
        self.lerp: float = 0.1
        self.rotation: float = 0.0
        self.parallax_force: float = 0.0
        self.parallax_speed: float = 0.0
        self.follow_delay: float = 0.0
        self.max_anchor_deviation: float = 0.0
        self.base_image: object = None
        self.resultant_image: object = None
        self.setup()
        
    def setup(self) -> None:
        self.manager.add_feature(self)

    def update(self, delta: float) -> None:
        self.velocity.x = lerp(self.sprite.position.x, self.predictor.predictions[self.label][0], self.lerp)
        self.velocity.y = lerp(self.sprite.position.y, self.predictor.predictions[self.label][1], self.lerp)

        self.velocity.x += self.feature['offset_x']
        self.velocity.y += self.feature['offset_y']
        
        self.sprite.position = self.velocity
        # self.sprite.position.x += self.sprite.width // 2

    def render(self, screen) -> None:
        self.sprite.render(screen)

