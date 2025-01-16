import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.__shot_timer = 0

    def triangle(self):
        forward = pygame.Vector2(0,1).rotate(self.rotation)
        right = pygame.Vector2(0,1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "yellow", self.triangle(), 2)

    def rotate(self, delta_time):
        self.rotation += PLAYER_TURN_SPEED * delta_time

    def move(self, delta_time):
        forward = pygame.Vector2(0,1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * delta_time

    def shoot(self):
        bullet = Shot(self.position.x, self.position.y)
        bullet.velocity =  pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.__shot_timer = PLAYER_SHOT_COOLDOWN

    def update(self, delta_time):

        self.__shot_timer -= delta_time
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.move(delta_time)
        if keys[pygame.K_s]:
            self.move(-delta_time)
        if keys[pygame.K_a]:
            self.rotate(-delta_time)
        if keys[pygame.K_d]:
            self.rotate(delta_time)
        if keys[pygame.K_SPACE] and self.__shot_timer <= 0:
            self.shoot()
