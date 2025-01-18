import pygame
from circleshape import CircleShape

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, health=30):
        super().__init__(x, y, radius)
        self.health = 30

    def takeDamage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.kill()


    def draw(self, screen):
        pygame.draw.circle(screen, "red", self.position, self.radius, 2)

    def update(self, delta_time):
        self.position += self.velocity * delta_time