import pygame
from Scripts.HitBoxObjects.circleshape import CircleShape
from ConstantVariables.constants import *

class TextObject(CircleShape):
    def __init__(self, position, text, speed=UI_TEXT_FLOAT_SPEED, fade=UI_TEXT_FADE_TIME):
        super().__init__(position.x, position.y, 0)
        self.velocity = pygame.Vector2(0,-1)
        self.timer_death = 0
        self.fade_time = fade
        self.speed = speed

        self.text = pygame.font.Font(None, UI_FONT_SIZE).render(text, True, UI_FONT_COLOR)

    def draw(self, screen):
        tet_rect = self.text.get_rect(center=(self.position.x, self.position.y))
        screen.blit(self.text, tet_rect)

    def update(self, delta_time):
        if self.timer_death >= self.fade_time:
            self.kill()
        self.position += self.velocity * self.speed * delta_time
        self.timer_death += delta_time
        