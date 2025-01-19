import pygame
import random
from circleshape import CircleShape
from constants import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, health=30):
        super().__init__(x, y, radius)
        self.health = health

    def takeDamage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.split()

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        random_degree_variance = random.uniform(20, 50)
        new_asteroid1_velocity = self.velocity.rotate(-random_degree_variance)
        new_asteroid2_velocity = self.velocity.rotate(random_degree_variance)
        new_asteroid_radius = self.radius - ASTEROID_MIN_RADIUS
        
        new_asteroid1 = Asteroid(self.position.x, self.position.y, new_asteroid_radius)
        new_asteroid1.velocity = new_asteroid1_velocity * 1.2

        new_asteroid2 = Asteroid(self.position.x, self.position.y, new_asteroid_radius)
        new_asteroid2.velocity = new_asteroid2_velocity * 1.2


    def draw(self, screen):
        pygame.draw.circle(screen, "red", self.position, self.radius, 2)

    def update(self, delta_time):
        self.position += self.velocity * delta_time


