import pygame
from lib import vector2

class Sprite:
    def __init__(self, image, position, width, height):
        self.position = position
        self.image = pygame.image.load(image)
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def render(self, screen):
        screen.blit(self.image, (self.position.x - self.width // 2, self.position.y - self.height // 2))

    def is_colliding(self, other):
        return (self.position.x < other.position.x + other.width and
                self.position.x + self.width > other.position.x and
                self.position.y < other.position.y + other.height and
                self.position.y + self.height > other.position.y)