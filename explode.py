import pygame
from shot import Shot

class Explode(Shot):
    def __init__(self, position, radius, dmg, spawned_on_enemy=None):
        super().__init__(position.x, position.y, radius, dmg)
        self.enemies_damaged = []
        if spawned_on_enemy != None:
            self.enemies_damaged.append(spawned_on_enemy)

    def draw(self, screen):
        pygame.draw.circle(screen, "red", self.position, self.radius, 0)