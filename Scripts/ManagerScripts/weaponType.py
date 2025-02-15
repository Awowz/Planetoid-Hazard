import pygame
import random
from ConstantVariables.constants import *
from Scripts.HitBoxObjects.InteractionObjects.shot import Shot
from Scripts.ManagerScripts.particleManager import ParticleManager
from Scripts.ManagerScripts.itemsList import ItemList
from Scripts.HitBoxObjects.temporaryTextObject import TextObject
from Scripts.ManagerScripts.audioManager import AudioManager
from Scripts.ManagerScripts.itemsList import ItemList

avaliable_weapons = [
    {"gun type": "smg", "fire rate": SMG_FIRE_RATE, "damage": SMG_DAMAGE, "bullet speed": SMG_SHOOT_SPEED, "radius": SMG_SHOT_RADIUS, "accuracy": SMG_ACCURACY, "bullet count": SMG_PELLETS,"ammo capacity": SMG_AMMO_CAPACITY, "reload time" : SMG_RELOAD},    
    {"gun type": "pistol", "fire rate": PISTOL_FIRE_RATE, "damage": PISTOL_DAMAGE, "bullet speed": PISTOL_SHOOT_SPEED, "radius": PISTOL_SHOT_RADIUS, "accuracy": PISTOL_ACCURACY, "bullet count": PISTOL_PELLETS, "ammo capacity": PISTOL_AMMO_CAPACITY, "reload time" : PISTOL_RELOAD},
    {"gun type": "shotgun", "fire rate": SHOTGUN_FIRE_RATE, "damage": SHOTGUN_DAMAGE, "bullet speed": SHOTGUN_SHOOT_SPEED, "radius": SHOTGUN_SHOT_RADIUS, "accuracy": SHOTGUN_ACCURACY, "bullet count": SHOTGUN_PELLETS, "ammo capacity": SHOTGUN_AMMO_CAPACITY, "reload time" : SHOTGUN_RELOAD},
]


class WeaponType(pygame.sprite.Sprite):
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.our_items_list = ItemList()

        self.__current_weapon_position = len(avaliable_weapons)
        self.shot_delay = None
        self.shot_damage = None
        self.active_gun = None
        self.shot_speed = None
        self.shot_radius = None
        self.shot_accuracy = None
        self.bullet_count = None
        self.ammo_capacity = 1
        self.reload_time = 1

        self.current_ammo = 1
        self.__weapon_swap_ammo_percent = None
        self.__weapon_swap_reload_percent = 1

        self.__time_passed = 0
        self.__time_passed_swapping = WEAPON_SWAP_DELAY + 1
        self.__time_passed_reloading = 0

        self.__isCurrently_releading = False

        self.swap_weapon()
        self.particleManager = ParticleManager()
        self.our_items_list = ItemList()
        self.our_audio_manager = AudioManager()

        
    def damageformula(self, player_level):
        dmg = self.shot_damage + ((self.shot_damage * player_level) / 2)
        return dmg


    def __getAccuracy(self):
        acc = self.shot_accuracy - self.our_items_list.getAccuracy()
        if acc <= 0.001:
            return 0.001
        return acc

    def __getBulletCount(self):
        pellets = self.bullet_count + self.our_items_list.getBulletCount()
        return pellets
    
    def __swapCurrentAmmo(self):
        self.current_ammo = self.__getMaxAmmoCap() * self.__weapon_swap_ammo_percent
    
    def __swapCurrentReloadTime(self):
        if self.__isCurrently_releading:
            self.__time_passed_reloading = self.__time_passed_reloading * self.__weapon_swap_reload_percent

            
    def __getMaxAmmoCap(self):
        return self.ammo_capacity + self.our_items_list.getAmmoCapacityCount()
    
    def __getReloadTime(self):
        return self.reload_time * self.our_items_list.getReloadModifer()
    
    def __getFireRate(self):
        return self.shot_delay * self.our_items_list.getFireRateModifer()

    def shoot(self, position, rotation, player_level=1):
        if self.current_ammo <= 0:
            self.__isCurrently_releading = True

        if self.__time_passed >= self.__getFireRate() and not self.__isCurrently_releading:
            self.current_ammo -= 1
            for x in range(self.__getBulletCount()):
                bullet = Shot(position.x, position.y, self.shot_radius, self.damageformula(player_level))
                bullet.velocity =  pygame.Vector2(0,1).rotate(rotation + random.uniform(-self.__getAccuracy(), self.__getAccuracy())) * self.shot_speed
                self.__time_passed = 0
                self.our_audio_manager.playAudioGunShot()

    def swap_weapon(self):
        if self.__time_passed_swapping < WEAPON_SWAP_DELAY:
            return    
        self.__time_passed_swapping = 0

        if self.__current_weapon_position >= (len(avaliable_weapons) - 1):
            self.__current_weapon_position = 0
        else:
            self.__current_weapon_position += 1

        self.__weapon_swap_ammo_percent = self.current_ammo / self.__getMaxAmmoCap()
        self.__weapon_swap_reload_percent = self.__time_passed_reloading / self.__getReloadTime()

        self.shot_delay = avaliable_weapons[self.__current_weapon_position]["fire rate"]
        self.shot_damage = avaliable_weapons[self.__current_weapon_position]["damage"]
        self.active_gun = avaliable_weapons[self.__current_weapon_position]["gun type"]
        self.shot_speed = avaliable_weapons[self.__current_weapon_position]["bullet speed"]
        self.shot_radius = avaliable_weapons[self.__current_weapon_position]["radius"]
        self.shot_accuracy = avaliable_weapons[self.__current_weapon_position]["accuracy"]
        self.bullet_count = avaliable_weapons[self.__current_weapon_position]["bullet count"]
        self.ammo_capacity = avaliable_weapons[self.__current_weapon_position]["ammo capacity"]
        self.reload_time = avaliable_weapons[self.__current_weapon_position]["reload time"]

        self.__swapCurrentAmmo()
        self.__swapCurrentReloadTime()

        TextObject(pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT), self.active_gun, UI_WEAPON_TEXT_SPEED, UI_WEAPON_TEXT_FADE)

    def update(self, delta_time):
        self.__time_passed += delta_time
        self.__time_passed_swapping += delta_time

        if self.__isCurrently_releading:
            self.__time_passed_reloading += delta_time
            if self.__time_passed_reloading > self.__getReloadTime():
                self.__isCurrently_releading = False
                self.__time_passed_reloading = 0
                self.current_ammo = self.__getMaxAmmoCap()

    def draw(self, screen):
        text = pygame.font.Font(None, UI_FONT_SIZE).render(f"{int(self.current_ammo)}/{self.__getMaxAmmoCap()}", True, UI_FONT_COLOR)
        screen.blit(text, pygame.Vector2(PLAYER_EXP_DISPLAY_POSITION_X, PLAYER_EXP_DISPLAY_POSITION_Y + UI_PLAYER_LVL_OFFSET * 2))


    def playerDependentDraw(self, screen, my_player):
        if self.__isCurrently_releading:
            pygame.draw.rect(screen, PLAYER_EXP_DISPLAY_BORDER_COLOR, [my_player.position.x - round(PLAYER_RELOAD_DISPLAY_LENGTH / 2), my_player.position.y + round(PLAYER_RELOAD_DISPLAY_HEIGHT * 7), PLAYER_RELOAD_DISPLAY_LENGTH + PLAYER_RELOAD_DISPLAY_BORDER, PLAYER_RELOAD_DISPLAY_HEIGHT + PLAYER_RELOAD_DISPLAY_BORDER], 0)
            normalize_length = (self.__time_passed_reloading + 0.01) / self.__getReloadTime()
            pygame.draw.rect(screen, EXP_COLOR, [my_player.position.x - round(PLAYER_RELOAD_DISPLAY_LENGTH / 2), my_player.position.y + round(PLAYER_RELOAD_DISPLAY_HEIGHT * 7), PLAYER_RELOAD_DISPLAY_LENGTH * normalize_length, PLAYER_RELOAD_DISPLAY_HEIGHT])

