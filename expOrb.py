import pygame
from circleshape import CircleShape
from constants import *

class ExpOrb(CircleShape):
    def __init__(self, position, exp_amount):
        super().__init__(position.x, position.y, EXP_HIT_BOX_RADIUS)
        self.exp_amount = exp_amount
        self.__has_touched_players_magnet = False
        self.currect_rotation = 0
        self.player_position = pygame.Vector2(0,0)
    
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

    def move_to_player(self, player):
        if self.__has_touched_players_magnet:
            #TODO
            pass
            
    
    def checkCollision(self, target):
        distance = self.position.distance_to(target.position)
        is_collided = distance <= self.radius + target.exp_radius_magnet
        
        if is_collided:
            self.player_position = target.position
            self.__has_touched_players_magnet = True
            self.__grantExp(target)##TODO MOVE TO PLAYER
        return is_collided
    
    def __grantExp(self, player):
        player.gainExp(self.exp_amount)
        self.kill()