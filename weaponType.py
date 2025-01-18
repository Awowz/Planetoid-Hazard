import pygame
from constants import *
from shot import Shot

avaliable_weapons = [
    {"gun type": "pistol", "fire rate": PISTOL_FIRE_RATE, "damage": PISTOL_DAMAGE},
    {"gun type": "smg", "fire rate": SMG_FIRE_RATE, "damage": SMG_DAMAGE},
]


class WeaponType(pygame.sprite.Sprite):
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.__current_weapon_position = len(avaliable_weapons)
        self.shot_speed = None
        self.shot_damage = None
        self. active_gun = None
        self.swap_weapon()

        self.__time_passed = 0
        

    def shoot(self, position, rotation):
        if self.__time_passed >= self.shot_speed:
            bullet = Shot(position.x, position.y)
            bullet.velocity =  pygame.Vector2(0,1).rotate(rotation) * PLAYER_SHOOT_SPEED
            self.__time_passed = 0


    def swap_weapon(self):
        if self.__current_weapon_position == len(avaliable_weapons):
            self.__current_weapon_position = 0
        else:
            self.__current_weapon_position += 1

        self.shot_speed = avaliable_weapons[self.__current_weapon_position]["fire rate"]
        self.shot_damage = avaliable_weapons[self.__current_weapon_position]["damage"]
        self.active_gun = avaliable_weapons[self.__current_weapon_position]["gun type"]

    def update(self, delta_time):
        self.__time_passed += delta_time