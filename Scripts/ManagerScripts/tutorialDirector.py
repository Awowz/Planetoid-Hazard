import pygame
import random
from ConstantVariables.constants import *
from Scripts.HitBoxObjects.EnemyObjects.asteroidEnemy import AsteroidEnemy
from Scripts.HitBoxObjects.InteractionObjects.expOrb import ExpOrb
from Scripts.HitBoxObjects.EnemyObjects.meleeEnemy import MeleeEnemy
from Scripts.ManagerScripts.itemsList import ItemList

class TutorialDirector(pygame.sprite.Sprite):
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.current_action = 0
        self.dummy_target = None
        self.single_spawn = False
        self.display_text = ""
        self.display_text_2 = ""
        self.font = pygame.font.Font(None, TUTORIAL_TEXT_SIZE)
        self.time_elicped = TUTORIAL_STEP_DELAY

        self.our_item_list = ItemList()

    def __resetForNextStep(self):
        self.dummy_target = None
        self.single_spawn = False
        self.current_action += 1
        self.display_text = ""
        self.display_text_2 = ""
        self.time_elicped = TUTORIAL_STEP_DELAY

    def is_player_ready(self) ->bool:
        keys = pygame.key.get_pressed()
        return (keys[pygame.K_x] and self.time_elicped <= 0)
        
    def checkProgress(self, delta_time):
        if self.current_action == 0: 
            self.display_text = "W A S D to move and SPACE to shoot. Hold Shift to slow turn"
            self.display_text_2 = "Kill the red target at the bottom left"
            if self.dummy_target == None and not self.single_spawn:
                self.dummy_target = AsteroidEnemy(SCREEN_WIDTH / 10, SCREEN_HEIGHT / 1.1, 20, pygame.Vector2(0,0), 0, add_health=-25, add_exp_drop=0)
                self.single_spawn =True
            if self.dummy_target.health <= 0:
                self.__resetForNextStep()
        if self.current_action == 1:
            self.display_text = "Pick up EXP orb to level up"
            if self.dummy_target == None and not self.single_spawn:
                self.dummy_target = ExpOrb(pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), 35)
                self.single_spawn = True
            if self.dummy_target.has_touched_players_magnet and self.single_spawn:
                self.__resetForNextStep()
        if self.current_action == 2:
            self.display_text = "Levels grant items, press TAB and use your mouse to select any reward"    
            self.display_text_2 = "Press X to continue"        
            if self.is_player_ready():
                self.__resetForNextStep()
        if self.current_action == 3:
            self.display_text = "Items will enhance your survivability, picking up more of the same item stacks its effects."
            self.display_text_2 = "Press X to continue"
            if self.is_player_ready():
                self.__resetForNextStep()
        if self.current_action == 4:
            self.display_text = "All items synergises with specific items or a specific weapon"
            self.display_text_2 = "Press X to continue"
            if self.is_player_ready():
                self.__resetForNextStep()                    
        if self.current_action == 5:
            if not self.single_spawn:
                for x in self.our_item_list.all_items:
                    self.our_item_list.increase_count_of_item(x)
                self.single_spawn = True
            self.display_text = "Youve been given all items. Press ESC to see the items you picked it."
            self.display_text_2 = "Hovering the item lets you read the items details  Press X to continue"
            if self.is_player_ready():
                self.__resetForNextStep()
        if self.current_action == 6:
            self.display_text = "You have different weapons, press E to swap between them"
            self.display_text_2 = "Press X to continue"
            if self.is_player_ready():
                self.__resetForNextStep()            
        if self.current_action == 7:
            self.display_text = "Enemies scale over time becoming harder to kill, with more of them spawning over time"
            self.display_text_2 = "Press X to continue"
            if self.is_player_ready():
                self.__resetForNextStep()
        if self.current_action == 8:
            
            self.display_text = "Tutorial completed, good luck!"
            if self.time_elicped <= 0:
                for x in range(100):
                    MeleeEnemy(random.randint(0, SCREEN_WIDTH),0, MELEE_RADIUS, (0,1), MELEE_SPEED, MELEE_COLOR, 200, 0)
                    MeleeEnemy(random.randint(0, SCREEN_WIDTH),SCREEN_HEIGHT, MELEE_RADIUS, (0,1), MELEE_SPEED, MELEE_COLOR, 200, 0)
                    MeleeEnemy(0,random.randint(0, SCREEN_HEIGHT), MELEE_RADIUS, (0,1), MELEE_SPEED, MELEE_COLOR, 200, 0)
                    MeleeEnemy(SCREEN_WIDTH,random.randint(0, SCREEN_HEIGHT), MELEE_RADIUS, (0,1), MELEE_SPEED, MELEE_COLOR, 200, 0)
                self.current_action += 1

        self.time_elicped -= delta_time
            
            

    def draw(self, screen):
        output = self.font.render(self.display_text, True, UI_FONT_COLOR)
        output_rect = output.get_rect(center=(SCREEN_WIDTH / 2, TUTORIAL_TEXT_Y_OFFSET))
        screen.blit(output, output_rect)

        output2 = self.font.render(self.display_text_2, True, UI_FONT_COLOR)
        output_rect2 = output2.get_rect(center=(SCREEN_WIDTH / 2, TUTORIAL_TEXT_Y_OFFSET + TUTORIAL_TEXT_SECOND_LINE_Y_OFFSET))
        screen.blit(output2, output_rect2)