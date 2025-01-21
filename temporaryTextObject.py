import pygame
from circleshape import CircleShape
from constants import *

class TextObject(CircleShape):
    def __init__(self, position, text):
        super().__init__(position.x, position.y, 0)
        self.velocity = pygame.Vector2(0,-1)
        self.timer_death = 0

        self.text = pygame.font.Font(None, UI_FONT_SIZE).render(text, True, UI_FONT_COLOR)

    def draw(self, screen):
        screen.blit(self.text, self.position)

    def update(self, delta_time):
        if self.timer_death >= UI_TEXT_FADE_TIME:
            self.kill()
        self.position += self.velocity * UI_TEXT_FLOAT_SPEED * delta_time
        self.timer_death += delta_time
        