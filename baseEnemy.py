import pygame
from circleshape import CircleShape
from expOrb import ExpOrb

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

    ##for drawing
    def draw(self, screen):
        pass 

    #for updating objects game logic
    def update(self, dt):
        pass

    #for setting a path to a target locaition
    def pathing(self, target):
        pass