import pygame
from Scripts.HitBoxObjects.circleshape import CircleShape
from ConstantVariables.constants import *

class Mouse(CircleShape):
    def __init__(self):
        super().__init__(1, 1, MOUSE_HITBOX)

    def update(self, dt):
        self.generalUpdate(dt)

    def pauseUpdate(self, dt):
        self.generalUpdate(dt)

    def generalUpdate(self, dt):
        self.position = pygame.Vector2(pygame.mouse.get_pos())
        