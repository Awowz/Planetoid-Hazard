from circleshape import CircleShape
from constants import *
import pygame

class Shot(CircleShape):
    def __init__(self, x, y, radius, dmg):
        super().__init__(x, y, radius)
        self.damage = dmg

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)
    
    def update(self, delta_time):
        self.position += self.velocity * delta_time
        
        if self.position.x <= -BORDER_KILL_ZONE_X or BORDER_KILL_ZONE_X + SCREEN_WIDTH < self.position.x:
            self.kill()
        if self.position.y <= -BORDER_KILL_ZONE_Y or BORDER_KILL_ZONE_Y + SCREEN_HEIGHT < self.position.y:
            self.kill()