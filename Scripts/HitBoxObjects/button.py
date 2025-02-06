import pygame
from Scripts.HitBoxObjects.circleshape import CircleShape
from ConstantVariables.constants import *

class Button(CircleShape):
    def __init__(self, position, text, callFunction):
        super().__init__(position.x, position.y, BUTTON_HITBOX)
        self.function_to_callback = callFunction
        self.text = text
        self.is_visable = False

        self.render_text = pygame.font.Font(None, UI_FONT_SIZE).render(self.text, True, UI_FONT_COLOR)
        self.render_text_rect = self.render_text.get_rect(center=(self.position.x, self.position.y))

    def __drawBlankBox(self, screen):
        top_left_pos = self.position + pygame.Vector2(-BUTTON_BOX_WIDTH, -BUTTON_BOX_HEIGHT)
        pygame.draw.rect(screen, PLAYER_EXP_DISPLAY_BORDER_COLOR, [top_left_pos.x, top_left_pos.y, BUTTON_BOX_WIDTH * 2, BUTTON_BOX_HEIGHT * 2], 0)
        
    def __draw_highlight(self,screen):
        top_left_pos = self.position + pygame.Vector2(-BUTTON_BOX_WIDTH, -BUTTON_BOX_HEIGHT)
        pygame.draw.rect(screen, EXP_COLOR, [top_left_pos.x, top_left_pos.y, BUTTON_BOX_WIDTH * 2, BUTTON_BOX_HEIGHT * 2], 2)
        

    def draw(self, screen):
        self.__drawBlankBox(screen)
        screen.blit(self.render_text, self.render_text_rect)
        if self.is_visable: self.__draw_highlight(screen)

    def callFunction(self, screen):
        self.function_to_callback(screen)

    def setNotVisable(self):
        self.is_visable = False
    def setVisable(self):
        self.is_visable = True