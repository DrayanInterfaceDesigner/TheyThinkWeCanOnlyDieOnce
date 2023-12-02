from lib import Vector2

class Feature:
    def __init__(self) -> None:
        position: Vector2 = Vector2().ZERO()
        acceleration: Vector2 = Vector2().ZERO()
        velocity: Vector2 = Vector2().ZERO()
        anchor: Vector2 = Vector2().ZERO()
        size: dict = {
            "width": 0.0,
            "height": 0.0
        }
        mass: float = 0.0
        radius: float = 0.0
        speed: float = 0.0
        max_speed: float = 0.0
        max_force: float = 0.0
        angle: float = 0.0
        rotation: float = 0.0
        parallax_force: float = 0.0
        parallax_speed: float = 0.0
        follow_delay: float = 0.0
        max_anchor_deviation: float = 0.0
        base_image: object = None
        resultant_image: object = None
        
    def setup(self) -> None:
        pass

    def update(self, delta: float) -> None:
        pass

    def render(self) -> None:
        pass

