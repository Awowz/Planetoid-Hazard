import pygame
from ConstantVariables.constants import *

class ItemTextBox(pygame.sprite.Sprite):
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        
        self.position = pygame.Vector2(ITEM_TEXT_BOX_CENTER_X, ITEM_TEXT_BOX_CENTER_Y)
        self.item_name_str = "..."
        self.item_desc_str = "..."
        self.font = pygame.font.Font(None, UI_FONT_SIZE)
        self.is_visable = False

    def setIsVisable(self, name, dsc):
        self.is_visable = True
        self.item_name_str = name
        self.item_desc_str = dsc

    def setNotVisable(self):
        self.is_visable = False

    def __drawBlankBox(self, screen):
        top_left_pos = self.position + pygame.Vector2(-ITEM_TEXT_BOX_WIDTH, -ITEM_TEXT_BOX_HEIGHT)
        pygame.draw.rect(screen, PLAYER_EXP_DISPLAY_BORDER_COLOR, [top_left_pos.x, top_left_pos.y, ITEM_TEXT_BOX_WIDTH * 2, ITEM_TEXT_BOX_HEIGHT * 2], 0)
        
    def draw(self, screen):
        if not self.is_visable: return
        self.__drawBlankBox(screen)

        item_name = self.font.render(self.item_name_str, True, UI_FONT_COLOR)
        item_desc = self.font.render(self.item_desc_str, True, UI_FONT_COLOR)
        item_name_rect = item_name.get_rect(center=(self.position.x, self.position.y - ITEM_TEXT_Y_OFFSET))
        item_desc_rect = item_desc.get_rect(center=(self.position.x, self.position.y + ITEM_TEXT_Y_OFFSET))
        screen.blit(item_name, item_name_rect)
        screen.blit(item_desc, item_desc_rect)

    def pauseDraw(self, screen):
        self.draw(screen)

    def pauseUpdate(self, delta_time):
        pass