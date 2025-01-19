import pygame
from circleshape import CircleShape
from constants import *

class ExpOrb(CircleShape):
    def __init__(self, position, exp_amount):
        super().__init__(position.x, position.y, EXP_HIT_BOX_RADIUS)
        self.exp_amount = exp_amount
        self.__has_touched_players_magnet = False
        self.currect_rotation = 45
    
    def rectangle(self):
        """
        new_bottom_left = pygame.Vector2(self.position.x - (EXP_SIZE_WIDTH / 2), self.position.y - (EXP_SIZE_HEIGHT))
        new_bottom_right = pygame.Vector2(self.position.x + (EXP_SIZE_WIDTH / 2), self.position.y - (EXP_SIZE_HEIGHT))
        new_top_left = pygame.Vector2(self.position.x - (EXP_SIZE_WIDTH / 2), self.position.y + (EXP_SIZE_HEIGHT))
        new_top_right = pygame.Vector2(self.position.x + (EXP_SIZE_WIDTH / 2), self.position.y + (EXP_SIZE_HEIGHT))
        """
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
    
    def collision_with_player(self, target):
        pass