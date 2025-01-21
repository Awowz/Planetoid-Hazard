from __future__ import annotations
import itemsList
import pygame
import os
from circleshape import CircleShape

from itemConstants import *

class ItemObject(CircleShape):
    def __init__(self, x, y, radius, item_str):
        super().__init__(x, y, radius)
        self.my_item_str = item_str
        self.our_item_list = itemsList.ItemList()
        self.imageObject = None
        self.getImage()

    def getImage(self):
        fileName =  self.my_item_str + ".png"
        filePath = ""
        try:
            filePath = os.path.join("Assets/", fileName)
            self.imageObject = pygame.image.load(filePath)
        except:
            print("error with image path")
            self.imageObject = pygame.image.load(PLACE_HOLDER_IMAGE)
        


    def draw(self, screen):
        screen.blit(self.imageObject, self.position)

    def checkCollision(self, target):##in main, change all_exp to all_pickups
        distance = self.position.distance_to(target.position)
        is_collided = distance <= self.radius + target.exp_radius_magnet
        if is_collided:
            self.givePlayerItem()

    def givePlayerItem(self):
        self.our_item_list.increase_count_of_item(self.my_item_str)
        #TODO display on ui
        self.kill()