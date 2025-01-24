import pygame
from shot import Shot
from particleManager import ParticleManager

class Explode(Shot):
    def __init__(self, position, radius, dmg, spawned_on_enemy=None):
        super().__init__(position.x, position.y, radius, dmg)
        self.enemies_damaged = None
        self.haveIExploded = False
        if spawned_on_enemy != None:
            self.enemies_damaged = spawned_on_enemy

    def draw(self, screen):
        pygame.draw.circle(screen, "red", self.position, self.radius, 0)

    def isTargetAlreadyTakenDamage(self, target):
        return (self.enemies_damaged == target)

    def update(self, delta_time):
        if self.haveIExploded:
            ParticleManager.explosion(ParticleManager(),self.position)
            self.kill()

        self.haveIExploded = True