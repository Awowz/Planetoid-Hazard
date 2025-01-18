import pygame
import random
from constants import *
from shot import Shot
from particleManager import ParticleManager

avaliable_weapons = [
    {"gun type": "pistol", "fire rate": PISTOL_FIRE_RATE, "damage": PISTOL_DAMAGE, "bullet speed": PISTOL_SHOOT_SPEED, "radius": PISTOL_SHOT_RADIUS, "accuracy": PISTOL_ACCURACY},
    {"gun type": "smg", "fire rate": SMG_FIRE_RATE, "damage": SMG_DAMAGE, "bullet speed": SMG_SHOOT_SPEED, "radius": SMG_SHOT_RADIUS, "accuracy": SMG_ACCURACY},
]


class WeaponType(pygame.sprite.Sprite):
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.__current_weapon_position = len(avaliable_weapons)
        self.shot_delay = None
        self.shot_damage = None
        self.active_gun = None
        self.shot_speed = None
        self.shot_radius = None
        self.shot_accuracy = None

        self.__time_passed = 0
        self.__time_passed_swapping = WEAPON_SWAP_DELAY + 1


        self.swap_weapon()
        self.particleManager = ParticleManager()

        
        

    def shoot(self, position, rotation):
        if self.__time_passed >= self.shot_delay:
            bullet = Shot(position.x, position.y, self.shot_radius)
            bullet.velocity =  pygame.Vector2(0,1).rotate(rotation + random.randint(-self.shot_accuracy, self.shot_accuracy)) * self.shot_speed
            self.__time_passed = 0
            self.particleManager.create_standard_particle(position, 1, pygame.Vector2(0,1).rotate(rotation) * (self.shot_speed / 2), 30)
        


    def swap_weapon(self):
        if self.__time_passed_swapping < WEAPON_SWAP_DELAY:
            return    
        self.__time_passed_swapping = 0

        if self.__current_weapon_position >= (len(avaliable_weapons) - 1):
            self.__current_weapon_position = 0
        else:
            self.__current_weapon_position += 1

        self.shot_delay = avaliable_weapons[self.__current_weapon_position]["fire rate"]
        self.shot_damage = avaliable_weapons[self.__current_weapon_position]["damage"]
        self.active_gun = avaliable_weapons[self.__current_weapon_position]["gun type"]
        self.shot_speed = avaliable_weapons[self.__current_weapon_position]["bullet speed"]
        self.shot_radius = avaliable_weapons[self.__current_weapon_position]["radius"]
        self.shot_accuracy = avaliable_weapons[self.__current_weapon_position]["accuracy"]

    def update(self, delta_time):
        self.__time_passed += delta_time
        self.__time_passed_swapping += delta_time

    def getDamage(self):
        return self.shot_damage