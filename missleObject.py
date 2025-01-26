import pygame
import math
from shot import Shot
from constants import *
from particleManager import ParticleManager

class Missle(Shot):
    def __init__(self, position, dmg):
        super().__init__(position.x, position.y, POCKET_MISSLE_RADIUS, dmg)
        self.rotation = 0
        self.speed = POCKET_MISSLE_SPEED

    def rectangle(self):
        forward = pygame.Vector2(0,1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 2.5

        new_bottom_left = self.position - forward * self.radius - right
        new_bottom_right = self.position - forward * self.radius + right
        new_top_right = self.position + forward * self.radius - right
        new_top_left = self.position + forward * self.radius + right
        
        return [ new_bottom_right, new_bottom_left,new_top_right,new_top_left]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.rectangle())

    def update(self, delta_time):
        pass

    def pathing(self, target: pygame.Vector2, delta_time):
        distance_x = target.x - self.position.x
        distance_y = target.y - self.position.y
        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
        velocity = pygame.Vector2(distance_x / distance, distance_y / distance)
        if distance != 0:
            self.position += velocity * self.speed * delta_time
        radians = math.atan2(distance_x, distance_y)
        self.rotation = math.degrees(radians)*-1

        forward = pygame.Vector2(0,1).rotate(self.rotation)
        back_pos = self.position - forward * self.radius
        ParticleManager().create_particle_thrust(back_pos, self.rotation)
                    