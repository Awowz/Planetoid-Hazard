import pygame
from circleshape import CircleShape
from constants import *
from particleManager import ParticleManager
from weaponType import WeaponType

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.particleManager = ParticleManager()
        self.current_weapon = WeaponType()

    def triangle(self):
        forward = pygame.Vector2(0,1).rotate(self.rotation)
        right = pygame.Vector2(0,1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "yellow", self.triangle(), 0)

    def rotate(self, delta_time):
        self.rotation += PLAYER_TURN_SPEED * delta_time

    def move(self, delta_time):
        forward = pygame.Vector2(0,1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * delta_time
        back_triangle_position = self.position - pygame.Vector2(0,1).rotate(self.rotation) * self.radius
        self.particleManager.create_particle_thrust(back_triangle_position, self.rotation)

    def shoot(self):
        self.current_weapon.shoot(self.position, self.rotation)

    def update(self, delta_time):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.move(delta_time)
        if keys[pygame.K_s]:
            self.move(-delta_time)
        if keys[pygame.K_a]:
            self.rotate(-delta_time)
        if keys[pygame.K_d]:
            self.rotate(delta_time)
        if keys[pygame.K_SPACE]:
            self.shoot()
