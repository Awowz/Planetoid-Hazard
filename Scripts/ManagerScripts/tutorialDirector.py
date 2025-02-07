import pygame
from ConstantVariables.constants import *
from Scripts.HitBoxObjects.EnemyObjects.asteroidEnemy import AsteroidEnemy

class TutorialDirector(pygame.sprite.Sprite):
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.current_action = 0
        self.dummy_target = None
        self.single_spawn = False
        
    def checkProgress(self, delta_time):
        if self.current_action == 0: #create class that has a collosion that just hecks tto see if player has crossed them
            #print("wasd to move, space to shoot. shoot enemy to continue")

            if self.dummy_target == None and not self.single_spawn:
                self.dummy_target = AsteroidEnemy(SCREEN_WIDTH / 10, SCREEN_HEIGHT / 1.1, 20, pygame.Vector2(0,0), 0, add_health=-25, add_exp_drop=30)
                self.single_spawn =True
                print("enemy spawned") #inform player how to move and how to shoot. tell them to kill target
            if self.dummy_target .health <= 0:
                print("target elimainated") #tell them to pick up exp. make a hitbox object to check if player picked up exp
                self.current_action += 1
            

    def draw(self, screen):
        pass