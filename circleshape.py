import pygame
from constants import *

class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x,y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
    
    def draw(self, screen):
        pass

    def update(self, dt):
        if self.position.x <= -BORDER_KILL_ZONE_X or BORDER_KILL_ZONE_X + SCREEN_WIDTH < self.position.x:
            self.kill()
        if self.position.y <= -BORDER_KILL_ZONE_Y or BORDER_KILL_ZONE_Y + SCREEN_HEIGHT < self.position.y:
            self.kill()

    def checkCollision(self, target):
        distance = self.position.distance_to(target.position)
        is_object_collided = distance <= self.radius + target.radius
        return is_object_collided

    def kill(self):
        super().kill()
        del self