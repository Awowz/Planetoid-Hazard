import pygame
import random
import math
from ConstantVariables.constants import *
from ConstantVariables.itemConstants import *
from Scripts.HitBoxObjects.InteractionObjects.itemObject import ItemObject

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
            THREADED_BARREL_NAME : {COUNT : 0, DESCRIPTION: f"Accuracy of shots increased by {(THREADED_BARREL_VALUE * 10)}%", RARITY : WHITE},
            TRIGGER_FINGER_NAME : {COUNT : 0, DESCRIPTION: f"Firerate increased by {TRIGGER_FINGER_VALUE}%", RARITY : WHITE},
            MAGNET_NAME : {COUNT : 0, DESCRIPTION: f"Increases range of xp pickup by {MAGNET_VALUE} feet", RARITY : WHITE},
            #increase movement
            SPEED_LOADER_NAME : {COUNT : 0, DESCRIPTION: f"Increases reload speed by {SPEED_LOADER_VALUE}%", RARITY : WHITE},
            BANANA_MAG_NAME : {COUNT : 0, DESCRIPTION: f"Increases magazine capacity {BANANA_MAG_VALUE} shots", RARITY : WHITE},
            ##########on death items##########
            DUD_AIRSTRIKE_NAME : {COUNT : 0, DESCRIPTION: f"On enemy death there is a {DUD_AIRSTRIKE_ODDS}% chance for enemys to explode {DUD_AIRSTRIKE_DMG}", RARITY : GREEN},
            BLOOD_SUSTAINED_SHIELD_NAME : {COUNT : 0, DESCRIPTION: f"Kills will grant a {BLOOD_SUSTAINED_SHIELD_VALUE} second long sheild", RARITY : RED},
            #burn damage aoe
            #drop orb of sheild (10 orbs grants 1 shield) (can stack shield, shield kills and breaks)
            ##########on hit##########
            #knockbak
            #each accurate shot can have a chance of going back into the mag
            #10% to do double damage
            GOO_GLIME_NAME : {COUNT : 0, DESCRIPTION: f"On hit, reduce enemy movement by {GOO_GLIME_VALUE}%", RARITY : GREEN},
            POCKET_SAND_NAME : {COUNT : 0, DESCRIPTION: f"On hit, {POCKET_SAND_ODDS}% chance to stun enemy for {POCKET_SAND_DURATION} seconds", RARITY : GREEN},
            #blead
            POCKET_MISSLE_NAME : {COUNT : 0, DESCRIPTION: f"On hit, {POCKET_MISSLE_ODDS}% chance to shoot a homing missle", RARITY : GREEN},
            EXTRA_GUNPOWDER_NAME : {COUNT : 0, DESCRIPTION: f"All shots are now explode on impact", RARITY : RED},
            ##########uniques##########
            GHOST_LOADING_NAME : {COUNT : 0, DESCRIPTION: f"{GHOST_LOADING_VALUE}% chance to shoot another bullet", RARITY : GREEN},
            #accuracy shots (each shot that lands increases damage of next shot, if bullet hits kill wall. rest)
            ARMOR_CHIPPER_NAME : {COUNT : 0, DESCRIPTION: f"Enemies above {ARMOR_CHIPPER_THRESHOLD}% health take {(ARMOR_CHIPPER_VALUE * 100)}% more damage", RARITY: GREEN},
            ARMOR_PIERCING_ROUNDS_NAME: {COUNT : 0, DESCRIPTION: f"Bullets will now peice enemies", RARITY : GREEN},
            #spawn landmine every tower cycle
            #spawn turret
            #first bullet in mag does 100% damage
            #black hole, enemies get sucked into it
            #increase aoe size? hydogen tank?
            
            
        }
        self.obtained_itmes = set()

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
        self.obtained_itmes.add(str)

    def spawn_item(self, position):
        list_of_items_to_pick = self.__get_rarity_list(self.__rarity_pick())

        item_to_spawn = self.__get_pick_item(list_of_items_to_pick)

        return ItemObject(position.x, position.y, 20, item_to_spawn, self.all_items[item_to_spawn][DESCRIPTION])

    def getAccuracy(self) ->float:
        return self.all_items[THREADED_BARREL_NAME][COUNT] * THREADED_BARREL_VALUE
    
    def getAmmoCapacityCount(self) ->int:
        return self.all_items[BANANA_MAG_NAME][COUNT] * BANANA_MAG_VALUE

    def getGunPowderAOE(self) ->float:
        return self.all_items[EXTRA_GUNPOWDER_NAME][COUNT] * EXTRA_GUNPOWDER_RADIUS
    
    def getShieldDurration(self) ->float:
        if self.all_items[BLOOD_SUSTAINED_SHIELD_NAME][COUNT] == 0: return 0
        return BLOOD_SUSTAINED_SHIELD_VALUE + (2 * math.log(self.all_items[BLOOD_SUSTAINED_SHIELD_NAME][COUNT]))
    
    def getReloadModifer(self) ->float:
        if self.all_items[SPEED_LOADER_NAME][COUNT] == 0: return 1
        return (1 / (1 + (SPEED_LOADER_VALUE / 100) * self.all_items[SPEED_LOADER_NAME][COUNT]))
    
    def getFireRateModifer(self) ->float:
        if self.all_items[TRIGGER_FINGER_NAME][COUNT] == 0: return 1
        return (1 / (1 + (TRIGGER_FINGER_VALUE / 100) * self.all_items[TRIGGER_FINGER_NAME][COUNT]))
    
    def getPierceAmount(self) ->int:
        return self.all_items[ARMOR_PIERCING_ROUNDS_NAME][COUNT] * ARMOR_PIERCING_ROUNDS_VALUE
    
    def getMovmentReductionPercent(self) ->float:
        if self.all_items[GOO_GLIME_NAME][COUNT] == 0: return 1
        return (1 / (1 + (GOO_GLIME_VALUE / 100) * self.all_items[GOO_GLIME_NAME][COUNT]))

    def canISpawnExpo(self) ->bool:
        if self.all_items[EXTRA_GUNPOWDER_NAME][COUNT] >= 1:
            return True
        return False
    
    def getArmorChippedDmg(self, health_percent, dmg):
        if self.all_items[ARMOR_CHIPPER_NAME][COUNT] == 0: return dmg
        if health_percent >= ARMOR_CHIPPER_THRESHOLD:
            return (self.all_items[ARMOR_CHIPPER_NAME][COUNT] * ARMOR_CHIPPER_VALUE) * dmg
        return dmg
    
    def isStunEnemy(self):
        if self.all_items[POCKET_SAND_NAME][COUNT] == 0: return False
        odds = (1 - 1 / (1 + (POCKET_SAND_ODDS / 100) * self.all_items[POCKET_SAND_NAME][COUNT])) * 100
        rng = random.randint(0,100)
        if round(odds) >= rng:
            return True
        return False
    
    def getStunDuration(self):
        return POCKET_SAND_DURATION



    def canISpawnDudExpo(self) ->bool:
        if self.all_items[DUD_AIRSTRIKE_NAME][COUNT] == 0: return False
        rng = random.randint(0,100)
        if rng <= DUD_AIRSTRIKE_ODDS:
            return True
        return False
    
    def canISpawnMissle(self) ->bool:
        if self.all_items[POCKET_MISSLE_NAME][COUNT] == 0: return False
        rng = random.randint(0,100)
        if rng <= POCKET_MISSLE_ODDS:
            return True
        return False
    
    def getMissleDmg(self) ->float:
        return self.all_items[POCKET_MISSLE_NAME][COUNT] * POCKET_MISSLE_DMG

    def getDudExploDmg(self) ->float:
        return self.all_items[DUD_AIRSTRIKE_NAME][COUNT] * DUD_AIRSTRIKE_DMG
    
    def getDudExploRadius(self) ->int:
        return DUD_AIRSTRIKE_RADIUS


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
