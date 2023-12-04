import math

class Vector2:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def __add__(self, other) :
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other) :
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other) :
        return Vector2(self.x * other.x, self.y * other.y)
    
    def __truediv__(self, other) :
        return Vector2(self.x / other.x, self.y / other.y)
    
    def __floordiv__(self, other) :
        return Vector2(self.x // other.x, self.y // other.y)
    
    def __mod__(self, other) :
        return Vector2(self.x % other.x, self.y % other.y)
    
    def __pow__(self, other) :
        return Vector2(self.x ** other.x, self.y ** other.y)
    
    def __lshift__(self, other) :
        return Vector2(self.x << other.x, self.y << other.y)
    
    def __rshift__(self, other) :
        return Vector2(self.x >> other.x, self.y >> other.y)
    
    def dot_product(self, other) :
        return self.x * other.x + self.y * other.y
    
    def cross_product(self, other) :
        return self.x * other.y - self.y * other.x
    
    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self) -> float:
        return self / self.magnitude()
    
    def distance(self, other) -> float:
        return (self - other).magnitude()
    
    def angle(self, other) -> float:
        return math.acos(self.dot_product(other) / (self.magnitude() * other.magnitude()))
    
    def ZERO():
        return Vector2(0, 0)
    
