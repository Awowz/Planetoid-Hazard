import pygame
from circleshape import CircleShape
from expOrb import ExpOrb
from particleManager import ParticleManager
from constants import *
from audioManager import AudioManager
from itemsList import ItemList
from explode import Explode

class BaseEnemy(CircleShape):
    def __init__(self, x, y, radius, velocity, speed, color, health, exp_drop):
        super().__init__(x, y, radius)
        self.velocity = velocity
        self.color = color
        self.health = health
        self.exp_drop = exp_drop
        self.speed = speed

        self.is_damage_indicated = False
        self.my_OG_color = self.color
        self.damage_indicator_max_time = ANIMATION_DAMAGE_INDICATOR_TIME
        self.current_damage_indicator_time = 0

        self.our_audio_manager = AudioManager()
        self.our_item_list = ItemList()

    def dropExpOrb(self):
        ExpOrb(self.position, self.exp_drop)
        
    def takeDamage(self, dmg):
        self.startDamageIndicator()
        self.health -= dmg
        self.our_audio_manager.playAudioImpact()
        if self.health < 0.001:
            self.kill()

    def startDamageIndicator(self):
        self.is_damage_indicated = True
        self.current_damage_indicator_time = 0

    def kill(self):
        r = abs(self.my_OG_color[0] - PARTICLE_ON_DEATH_COLOR_ADJUSTMENT)
        g = abs(self.my_OG_color[1] - PARTICLE_ON_DEATH_COLOR_ADJUSTMENT)
        b = abs(self.my_OG_color[2] - PARTICLE_ON_DEATH_COLOR_ADJUSTMENT)
        ParticleManager.on_death(ParticleManager(), self.position, (r,g,b),self.radius/2)
        self.dropExpOrb()

        if self.our_item_list.canISpawnDudExpo():
            Explode(self.position, self.our_item_list.getDudExploRadius(), self.our_item_list.getDudExploDmg(), self)

        return super().kill()
    
    def __changeColor(self):
        color_normilize = 1 - (self.current_damage_indicator_time / self.damage_indicator_max_time)
        color_modifier = DAMAGE_COLOR_CHANGE_INTINSITY * color_normilize
        new_color = (abs(self.my_OG_color[0] - color_modifier), abs(self.my_OG_color[1] - color_modifier), abs(self.my_OG_color[2] - color_modifier))
        self.color = new_color

    def updateTakeDamageIndicator(self, delta_time):
        if not self.is_damage_indicated: return
        
        if self.current_damage_indicator_time >= self.damage_indicator_max_time:
            self.is_damage_indicated = False
            self.current_damage_indicator_time = 0
            self.color = self.my_OG_color
            return
        self.__changeColor()
        
        self.current_damage_indicator_time += delta_time


    ##for drawing
    def draw(self, screen):
        pass 

    #for updating objects game logic
    def update(self, delta_time):
        super().update(delta_time)
        self.updateTakeDamageIndicator(delta_time)
        pass

    #for setting a path to a target locaition
    def pathing(self, target: pygame.Vector2, delta_time):
        pass