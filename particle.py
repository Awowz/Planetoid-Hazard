import pygame
from circleshape import CircleShape

class Particle(CircleShape):
    def __init__(self, x, y, radius, fade_time):
        super().__init__(x,y,radius)
        self.fade_time = fade_time
        self.time_elipced = 0

    def draw(self, screen):
        pygame.draw.circle(screen, (0,0,255), self.position, self.radius, 2)
        

    def update(self, delta_time):
        self.time_elipced += delta_time
        if self.time_elipced >= self.fade_time:
            self.kill()
        