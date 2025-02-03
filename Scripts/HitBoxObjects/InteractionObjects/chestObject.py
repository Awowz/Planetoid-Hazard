import pygame
from Scripts.HitBoxObjects.circleshape import CircleShape
from ConstantVariables.constants import *
from Scripts.ManagerScripts.itemsList import ItemList
from Scripts.HitBoxObjects.InteractionObjects.itemObject import ItemObject

class Chest(CircleShape):
    def __init__(self, position, radius=CHEST_RADIUS):
        super().__init__(position.x, position.y, radius)
        self.is_player_in_range = False
        self.our_items_list = ItemList()
        self.Item_interacted_with_pos = None

        self.contained_item = [self.our_items_list.spawn_item(pygame.Vector2(position.x + CHEST_DISTANCE_X, position.y)), self.our_items_list.spawn_item(position), self.our_items_list.spawn_item(pygame.Vector2(position.x - CHEST_DISTANCE_X, position.y))]
        for x in self.contained_item:
            x.setChestObjectToTrue()

        self.text = pygame.font.Font(None, UI_FONT_SIZE).render("F to pick up item", True, UI_FONT_COLOR)
        self.text_pos_offset = pygame.Vector2(-CHEST_TEXT_X_OFFSET,-CHEST_TEXT_Y_OFFSET)
        

    def draw(self, screen):
        super().draw(screen)
        if self.is_player_in_range:
            screen.blit(self.text, self.contained_item[self.Item_interacted_with_pos].position + self.text_pos_offset)

    def update(self, dt):
        super().update(dt)
        keys = pygame.key.get_pressed()
        if self.is_player_in_range and keys[pygame.K_f]:
            self.contained_item[self.Item_interacted_with_pos].givePlayerItem()
            self.kill()

    def kill(self):
        for x in self.contained_item:
            x.kill()
        super().kill()

    def checkCollision(self, target):
        for x in range(len(self.contained_item)):
            distance = self.contained_item[x].position.distance_to(target.position)
            return_bool = distance <= self.radius + target.radius
            if return_bool:
                self.Item_interacted_with_pos = x
                break

        if return_bool:
            self.is_player_in_range = True
        else:
            self.is_player_in_range = False
        return return_bool