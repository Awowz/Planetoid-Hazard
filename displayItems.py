import pygame
from itemsList import ItemList
from itemObject import ItemObject
from itemConstants import *
from constants import *


class DisplayItems():
    def __init__(self):
        self.our_list = ItemList()
        self.current_layer_items_objects = []
        self.start_of_list_position = pygame.Vector2(SCREEN_WIDTH / 6, SCREEN_HEIGHT / 2)
        self.__init_fill_items()
        
    
    def __init_fill_items(self):
        y_distance_down = -100
        X_distance_right = -100

        counter = 0
        for x in self.our_list.obtained_itmes:
            if (counter % ITEMS_PER_ROW) == 0: 
                y_distance_down += ITEMS_ROW_OFFSET
                X_distance_right = 0
            
            X_distance_right += ITMES_COLUM_OFFSET
            self.current_layer_items_objects.append(ItemObject(self.start_of_list_position.x + X_distance_right, self.start_of_list_position.y + y_distance_down,0,x, self.our_list.all_items[x][DESCRIPTION]))
            
            counter += 1

    def draw(self, screen):
        font = pygame.font.Font(None, UI_FONT_SIZE) #.render(text, True, UI_FONT_COLOR)
        for x in self.current_layer_items_objects:
            x.draw(screen)
            text = font.render(f"x {self.our_list.all_items[x.my_item_str][COUNT]}", True, UI_FONT_COLOR)
            screen.blit(text, x.position + ITEMS_DISPLAY_COUNT_OFFSET)

        

    def kill(self):
        for x in self.current_layer_items_objects:
            x.kill()


#TODO items "spawn" arnt drawn until after. maybe have this displayitmes class pass through each of its objetcs and display it object items aslo need to have a mouse hover method for displaying tis information