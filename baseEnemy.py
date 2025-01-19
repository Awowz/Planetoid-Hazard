import pygame
from circleshape import CircleShape
from expOrb import ExpOrb
from particleManager import ParticleManager
from constants import *

class BaseEnemy(CircleShape):
    def __init__(self, x, y, radius, velocity, color, health, exp_drop):
        super().__init__(x, y, radius)
        self.velocity = velocity
        self.color = color
        self.health = health
        self.exp_drop = exp_drop

    def dropExpOrb(self):
        ExpOrb(self.position, self.exp_drop)
        
    def takeDamage(self, dmg):
        self.health -= dmg
        if self.health < 0.001:
            self.kill()

    def kill(self):
        r = abs(self.color[0] - PARTICLE_ON_DEATH_COLOR_ADJUSTMENT)
        g = abs(self.color[1] - PARTICLE_ON_DEATH_COLOR_ADJUSTMENT)
        b = abs(self.color[2] - PARTICLE_ON_DEATH_COLOR_ADJUSTMENT)
        ParticleManager.on_death(ParticleManager(), self.position, (r,g,b),self.radius/2)
        return super().kill()

    ##for drawing
    def draw(self, screen):
        pass 

    #for updating objects game logic
    def update(self, dt):
        pass

    #for setting a path to a target locaition
    def pathing(self, target):
        pass