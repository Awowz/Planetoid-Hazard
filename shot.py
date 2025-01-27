from circleshape import CircleShape
from constants import *
from itemsList import ItemList
import pygame

class Shot(CircleShape):
    def __init__(self, x, y, radius, dmg):
        super().__init__(x, y, radius)
        self.damage = dmg
        self.our_items_list = ItemList()

        self.enemy_list = []
        self.times_pierced = 0

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)
    
    def update(self, delta_time):
        self.position += self.velocity * delta_time
        
        if self.position.x <= -BORDER_KILL_ZONE_X or BORDER_KILL_ZONE_X + SCREEN_WIDTH < self.position.x:
            self.kill()
        if self.position.y <= -BORDER_KILL_ZONE_Y or BORDER_KILL_ZONE_Y + SCREEN_HEIGHT < self.position.y:
            self.kill()

    def haveIAttackedThisTarget(self, target) ->bool:
        for x in self.enemy_list:
            if x == target:
                return True
        return False

    def incrementPierce(self, target):
        self.enemy_list.append(target)
        self.times_pierced += 1

    def checkCollision(self, target):
        has_target_collided = super().checkCollision(target)
        if not has_target_collided: return has_target_collided

        if self.times_pierced > self.our_items_list.getPierceAmount():
            self.kill()
            return has_target_collided
        elif self.haveIAttackedThisTarget(target):
            return False
        else:
            self.incrementPierce(target)
            return has_target_collided
            