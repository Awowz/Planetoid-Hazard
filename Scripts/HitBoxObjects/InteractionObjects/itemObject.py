from __future__ import annotations
import Scripts.ManagerScripts.itemsList as itemsList
import pygame
import os
import math
from Scripts.HitBoxObjects.circleshape import CircleShape
from Scripts.HitBoxObjects.temporaryTextObject import TextObject

from ConstantVariables.itemConstants import *
from ConstantVariables.constants import *

class ItemObject(CircleShape):
    def __init__(self, x, y, radius, item_str, item_desct, item_rarity=None):
        super().__init__(x, y, radius)
        self.original_pos_x, self.original_pos_y = self.position.x, self.position.y
        self.my_item_str = item_str
        self.item_desct = item_desct
        self.item_rarity = item_rarity
        self.our_item_list = itemsList.ItemList()
        self.image_offset = pygame.Vector2(-ITEM_IMAGE_X_OFFSET, -ITEM_IMAGE_Y_OFFSET)
        self.imageObject = None
        self.getImage()

        self.is_chest_item = False
        
        self.time_elapsed = 0
        self.speed = ITEM_BOUCE_SPEED
        self.scale = ITEM_BOUCE_SCALE

    def getImage(self):
        fileName =  self.my_item_str + ".png"
        filePath = ""
        try:
            filePath = os.path.join("Assets/", fileName)
            self.imageObject = pygame.image.load(filePath)
        except:
            print("error with image path")
            self.imageObject = pygame.image.load(PLACE_HOLDER_IMAGE)
        
    def setChestObjectToTrue(self):
        self.is_chest_item = True

    def draw(self, screen):
        if self.item_rarity != None: pygame.draw.rect(screen, ITEM_COLOR[self.item_rarity], [self.original_pos_x - (ITEM_BOX_WIDTH / 2), self.original_pos_y - (ITEM_BOX_HEIGHT / 2), ITEM_BOX_WIDTH, ITEM_BOX_HEIGHT])
        screen.blit(self.imageObject, self.position + self.image_offset)

    def checkCollision(self, target):##in main, change all_exp to all_pickups
        if self.is_chest_item: return
        distance = self.position.distance_to(target.position)
        is_collided = distance <= self.radius + target.exp_radius_magnet
        if is_collided:
            self.givePlayerItem()

    def givePlayerItem(self):
        self.our_item_list.increase_count_of_item(self.my_item_str)
        TextObject(self.position, f"{self.my_item_str}    {self.item_desct}")
        self.kill()

    def bounce(self):
        return math.cos(self.time_elapsed * self.speed / math.pi) * self.scale


    def update(self, delta_time):
        self.time_elapsed += delta_time
        self.position.y += self.bounce()