import pygame
import random
from constants import *

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
            "threaded barrel" : {COUNT : 0, DESCRIPTION: f"increases accuracy of shots by current count x {THREADED_BARREL}", RARITY : WHITE},
            #shoot faster
            #increase exp pickup range
            #increase movement
            ##########on death items##########
            "dud airstrike" : {COUNT : 0, DESCRIPTION: f"10% chance for enemys to explode on death dealing current count x {DUD_AIRSTRIKE_DMG}", RARITY : GREEN},
            #3 second shield
            #burn damage aoe
            #drop orb of sheild (10 orbs grants 1 shield) (can stack shield, shield kills and breaks)
            ##########on hit##########
            #10% to do double damage
            #slow
            #stun
            #blead
            #missle
            "extra gunpowder" : {COUNT : 0, DESCRIPTION: f"all shots are now AOE. radius is {EXTRA_GUNPOWDER_RADIUS} x current count", RARITY : RED},
            ##########uniques##########
            #shoot twice (20%)
            #accuracy shots (each shot that lands increases damage of next shot, if bullet hits kill wall. rest)
            #75% damage to enemeis above 90& health
            #spawn landmine every tower cycle
            #spawn turret
            
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

        #TODO CREATE INSTANCE object thats drawable and checks for player collision


    def list_all(self):
        for x in self.all_items:
            print(f"count: {self.all_items[x][COUNT]}    description: {self.all_items[x][DESCRIPTION]}")
