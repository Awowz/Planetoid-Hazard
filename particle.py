import pygame
from circleshape import CircleShape

class Particle(CircleShape):
    def __init__(self, x, y, radius, fade_time, thickness=2, color=(0,0,255)):
        super().__init__(x,y,radius)
        self.fade_time = fade_time
        self.time_elipced = 0
        self.deceleration = pygame.Vector2(0,0)
        self.color = color
        self.thickness = thickness

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius, self.thickness)
        

    def update(self, delta_time):
        self.time_elipced += delta_time
        self.position += self.velocity * delta_time
        self.velocity += self.deceleration * delta_time
        if self.time_elipced >= self.fade_time:
            self.kill()
            del self
        