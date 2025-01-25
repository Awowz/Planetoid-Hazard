import pygame
import sys
import random
from circleshape import CircleShape
from constants import *
from particleManager import ParticleManager

class PlayerDeathDraw(CircleShape):
    def __init__(self, position):
        super().__init__(position.x, position.y, 0)
        ParticleManager.on_death(ParticleManager(), position, EXP_COLOR,69)

        self.time_passed = 0
        self.text = pygame.font.Font(None, PLAYER_DEATH_UI_FONT).render("GAME OVER", True, UI_FONT_COLOR)
    
        temp = self.position
        self.position = [temp - pygame.Vector2(4,0),temp + pygame.Vector2(4,0),temp - pygame.Vector2(0,3)]

        self.velocity = [None for x in range(3)]
        self.speed = [PLAYER_DEATH_DEBREE_SPEED for x in range(3)]
        self.rotation_speed = [PLAYER_DEATH_ROTATION_SPEED for x in range(3)]
        for x in range(3):
            self.velocity[x] = pygame.Vector2(0,1).rotate(random.randint(0,360))
            self.speed[x] = self.speed[x] * random.uniform(0.2,1.5)
            self.rotation_speed[x] = self.rotation_speed[x] * random.uniform(0.2,2.2)
        self.rotation = [0 for x in range(3)]
    


    def draw(self, screen):
        for x in range(3):
            front = pygame.Vector2(0,1).rotate(self.rotation[x])
            a = self.position[x] + front * PLAYER_RADIUS
            b = self.position[x] - front * PLAYER_RADIUS
            pygame.draw.line(screen, "yellow", a,b,3)

        screen.blit(self.text, pygame.Vector2((SCREEN_WIDTH / 2) + PLAYER_DEATH_UI_XOFFSET, (SCREEN_HEIGHT / 2) + PLAYER_DEATH_UI_YOFFSET))

    def update(self, delta_time):
        self.time_passed += delta_time
        for x in range(3):
            self.rotation[x] += self.rotation_speed[x] * delta_time
            self.position[x] += self.velocity[x] * self.speed[x] * delta_time
        if self.time_passed >= PLAYER_DEATH_TIMER:
            sys.exit()