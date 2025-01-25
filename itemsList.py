import pygame
import random
from constants import *
from itemConstants import *
from itemObject import ItemObject

class ItemList():
    _instance = None

    def __new__(cls): #singleton pattern
        if cls._instance is None:
            cls._instance = super(ItemList, cls).__new__(cls)
            cls._instance.init_inventory()
        return cls._instance

    def init_inventory(self):
        self.all_items = {
            ##########general stat upgrades##########
            THREADED_BARREL_NAME : {COUNT : 0, DESCRIPTION: f"increases accuracy of shots by current count x {THREADED_BARREL_VALUE}", RARITY : WHITE},
            #shoot faster
            MAGNET_NAME : {COUNT : 0, DESCRIPTION: f"increases range of xp pickup by current count x {MAGNET_VALUE}", RARITY : WHITE},
            #increase movement
            #reload speed
            BANANA_MAG_NAME : {COUNT : 0, DESCRIPTION: f"increases magazine capacity by current count x {BANANA_MAG_VALUE}", RARITY : WHITE},
            ##########on death items##########
            DUD_AIRSTRIKE_NAME : {COUNT : 0, DESCRIPTION: f"10% chance for enemys to explode on death dealing current count x {DUD_AIRSTRIKE_DMG}", RARITY : GREEN},
            #3 second shield
            #burn damage aoe
            #drop orb of sheild (10 orbs grants 1 shield) (can stack shield, shield kills and breaks)
            ##########on hit##########
            #each accurate shot can have a chance of going back into the mag
            #10% to do double damage
            #slow
            #stun
            #blead
            #missle
            EXTRA_GUNPOWDER_NAME : {COUNT : 0, DESCRIPTION: f"all shots are now AOE. radius is {EXTRA_GUNPOWDER_RADIUS} x current count", RARITY : RED},
            ##########uniques##########
            GHOST_LOADING_NAME : {COUNT : 0, DESCRIPTION: f"chance to shoot twice when shooting, {GHOST_LOADING_VALUE}% x current count", RARITY : GREEN},
            #accuracy shots (each shot that lands increases damage of next shot, if bullet hits kill wall. rest)
            #75% damage to enemeis above 90& health
            #spawn landmine every tower cycle
            #spawn turret
            #first bullet in mag does 100% damage
            
            
        }
    def __rarity_pick(self) -> str:
        odds = random.uniform(0, 100)
        if odds >= GREEN_ODDS:
            return RED
        elif odds >= WHITE_ODDS:
            return GREEN
        return WHITE
    
    def __get_rarity_list(self, rarity_pick: str) -> list:
        list_of_items = []
        for x in self.all_items:
            if rarity_pick == self.all_items[x][RARITY]:
                list_of_items.append(x)
        return list_of_items
    
    def __get_pick_item(self, lst: list) -> str:
        item_index = random.randint(1, len(lst)) - 1
        return lst[item_index]

    def increase_count_of_item(self, str):
        self.all_items[str][COUNT] += 1

    def spawn_item(self, position):
        list_of_items_to_pick = self.__get_rarity_list(self.__rarity_pick())

        item_to_spawn = self.__get_pick_item(list_of_items_to_pick)

        ItemObject(position.x, position.y, 20, item_to_spawn, self.all_items[item_to_spawn][DESCRIPTION])

    def getAccuracy(self) ->float:
        return self.all_items[THREADED_BARREL_NAME][COUNT] * THREADED_BARREL_VALUE
    
    def getAmmoCapacityCount(self) ->int:
        return self.all_items[BANANA_MAG_NAME][COUNT] * BANANA_MAG_VALUE

    def getGunPowderAOE(self) ->float:
        return self.all_items[EXTRA_GUNPOWDER_NAME][COUNT] * EXTRA_GUNPOWDER_RADIUS

    def canISpawnExpo(self) ->bool:
        if self.all_items[EXTRA_GUNPOWDER_NAME][COUNT] >= 1:
            return True
        return False


    def getBulletCount(self) -> int:
        bullets_produced = 0
        bullet_odds = self.all_items[GHOST_LOADING_NAME][COUNT] * GHOST_LOADING_VALUE
        while bullet_odds >= 100:
            bullets_produced += 1
            bullet_odds -= 100
        odds = random.randint(1,100)
        if odds < bullet_odds:
            bullets_produced += 1
        return bullets_produced
    
    def getMagnetRadius(self):
        return self.all_items[MAGNET_NAME][COUNT] * MAGNET_VALUE


    def list_all(self):
        for x in self.all_items:
            print(f"count: {self.all_items[x][COUNT]}    description: {self.all_items[x][DESCRIPTION]}")
