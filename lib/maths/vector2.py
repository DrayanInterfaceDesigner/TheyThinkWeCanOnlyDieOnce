from lib import vector2
import math

class Vector2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: vector2) -> vector2:
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: vector2) -> vector2:
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other: vector2) -> vector2:
        return Vector2(self.x * other.x, self.y * other.y)
    
    def __truediv__(self, other: vector2) -> vector2:
        return Vector2(self.x / other.x, self.y / other.y)
    
    def __floordiv__(self, other: vector2) -> vector2:
        return Vector2(self.x // other.x, self.y // other.y)
    
    def __mod__(self, other: vector2) -> vector2:
        return Vector2(self.x % other.x, self.y % other.y)
    
    def __pow__(self, other: vector2) -> vector2:
        return Vector2(self.x ** other.x, self.y ** other.y)
    
    def __lshift__(self, other: vector2) -> vector2:
        return Vector2(self.x << other.x, self.y << other.y)
    
    def __rshift__(self, other: vector2) -> vector2:
        return Vector2(self.x >> other.x, self.y >> other.y)
    
    def dot_product(self, other: vector2) -> vector2:
        return self.x * other.x + self.y * other.y
    
    def cross_product(self, other: vector2) -> vector2:
        return self.x * other.y - self.y * other.x
    
    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self) -> float:
        return self / self.magnitude()
    
    def distance(self, other: vector2) -> float:
        return (self - other).magnitude()
    
    def angle(self, other: vector2) -> float:
        return math.acos(self.dot_product(other) / (self.magnitude() * other.magnitude()))
    
    def ZERO() -> vector2:
        return Vector2(0, 0)
    
