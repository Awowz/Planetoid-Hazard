import pygame
import random
from baseEnemy import BaseEnemy
from particleManager import ParticleManager
from constants import *

class AsteroidEnemy(BaseEnemy):
    def __init__(self, x, y, radius, velocity, color=ASTEROID_COLOR, add_health=0, add_exp_drop=0):
        super().__init__(x, y, radius, velocity, color, (ASTEROID_BASE_HEALTH + add_health), (ASTEROID_BASE_EXP_DROP + add_exp_drop))
        

    def takeDamage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            ParticleManager.on_death(ParticleManager(), self.position, self.radius/2)
            self.dropExpOrb()
            self.split()

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        random_degree_variance = random.uniform(20, 50)
        new_asteroid1_velocity = self.velocity.rotate(-random_degree_variance)
        new_asteroid2_velocity = self.velocity.rotate(random_degree_variance)
        new_asteroid_radius = self.radius - ASTEROID_MIN_RADIUS
        
        new_asteroid1 = AsteroidEnemy(self.position.x, self.position.y, new_asteroid_radius, new_asteroid1_velocity * 1.2, add_health=-10)

        new_asteroid2 = AsteroidEnemy(self.position.x, self.position.y, new_asteroid_radius, new_asteroid2_velocity * 1.2, add_health=-10)


    def draw(self, screen):
        pygame.draw.circle(screen, "red", self.position, self.radius, 2)

    def update(self, delta_time):
        self.position += self.velocity * delta_time


        