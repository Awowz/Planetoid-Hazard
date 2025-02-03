import pygame
import math
from Scripts.HitBoxObjects.EnemyObjects.baseEnemy import BaseEnemy
from ConstantVariables.constants import *

class MeleeEnemy(BaseEnemy):
    def __init__(self, x, y, radius, velocity, speed, color, add_health, add_exp_drop):
        super().__init__(x, y, radius, velocity, speed, color, add_health + MELEE_BASE_HEALTH, add_exp_drop + MELEE_BASE_EXP_DROP)
        self.rotation = 0

    def drawModel(self) ->list:
        forward = pygame.Vector2(0,1).rotate(self.rotation)
        right = pygame.Vector2(0,1).rotate(self.rotation + 90) * self.radius / 1.5

        p1 = self.position + forward * self.radius
        p2 = self.position - forward * self.radius - right
        p3 = self.position - forward * self.radius + right
        
        p4 = self.position - forward / 2 * self.radius
        return [p1,p2, p4, p3]
        

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.drawModel())

        

    def pathing(self, target: pygame.Vector2, delta_time):
        distance_x = target.x - self.position.x
        distance_y = target.y - self.position.y
        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
        velocity = pygame.Vector2(distance_x / distance, distance_y / distance)
        if distance != 0:
            self.position += velocity * self.speed * delta_time
        radians = math.atan2(distance_x, distance_y)
        self.rotation = math.degrees(radians)*-1
                    