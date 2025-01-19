import pygame
from circleshape import CircleShape
from constants import *

class ExpOrb(CircleShape):
    def __init__(self, position, exp_amount):
        super().__init__(position.x, position.y, EXP_HIT_BOX_RADIUS)
        self.exp_amount = exp_amount
        self.__has_touched_players_magnet = False
        self.currect_rotation = 0
    
    def rectangle(self):
        forward = pygame.Vector2(0,1).rotate(self.currect_rotation)
        right = pygame.Vector2(0, 1).rotate(self.currect_rotation + 90) * self.radius / 1.5

        new_bottom_left = self.position - forward * self.radius - right
        new_bottom_right = self.position - forward * self.radius + right
        new_top_right = self.position + forward * self.radius - right
        new_top_left = self.position + forward * self.radius + right
        
        return [new_bottom_left, new_bottom_right, new_top_right, new_top_left]

    def draw(self, screen):
        pygame.draw.polygon(screen, EXP_COLOR, self.rectangle())

    def update(self, delta_time):
        self.currect_rotation += EXP_ROTATION_SPEED * delta_time

    def move_to_player(self, player, delta_time):
        if self.__has_touched_players_magnet:
            if super().checkCollision(player):
                self.__grantExp(player)
            distance_x = player.position.x - self.position.x
            distance_y = player.position.y - self.position.y
            distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
            velocity = pygame.Vector2(distance_x / distance, distance_y / distance) * EXP_SPEED
            if distance != 0:
                self.position += velocity * delta_time
            
            
    
    def checkCollision(self, target):
        distance = self.position.distance_to(target.position)
        is_collided = distance <= self.radius + target.exp_radius_magnet
        
        if is_collided:
            self.__has_touched_players_magnet = True
        return is_collided
    
    def __grantExp(self, player):
        player.gainExp(self.exp_amount)
        self.kill()