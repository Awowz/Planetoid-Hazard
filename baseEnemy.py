import pygame
from circleshape import CircleShape

class BaseEnemy(CircleShape):
    def __init__(self, x, y, radius, speed, color, health, exp_drop):
        super.__init__(x, y, radius)
        self.speed = speed
        self.color = color
        self.health = health
        self.exp_drop = exp_drop

        
    def takeDamage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.kill()


    def draw(self, screen):
        pass

    def update(self, dt):
        pass