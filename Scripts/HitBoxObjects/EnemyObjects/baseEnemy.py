import pygame
from Scripts.HitBoxObjects.circleshape import CircleShape
from Scripts.HitBoxObjects.InteractionObjects.expOrb import ExpOrb
from Scripts.ManagerScripts.particleManager import ParticleManager
from ConstantVariables.constants import *
from Scripts.ManagerScripts.audioManager import AudioManager
from Scripts.ManagerScripts.itemsList import ItemList
from Scripts.HitBoxObjects.InteractionObjects.explode import Explode
from Scripts.ManagerScripts.screenShakeManager import ScreenShakeManager

class BaseEnemy(CircleShape):
    def __init__(self, x, y, radius, velocity, speed, color, health, exp_drop):
        super().__init__(x, y, radius)
        self.velocity = velocity
        self.color = color
        self.health = health
        self.max_health = health
        self.exp_drop = exp_drop
        self.max_speed = speed
        self.speed = self.max_speed
        self.is_currently_dying = False

        self.is_damage_indicated = False
        self.my_OG_color = self.color
        self.damage_indicator_max_time = ANIMATION_DAMAGE_INDICATOR_TIME
        self.current_damage_indicator_time = 0

        self.stun_duration = 0
        self.is_stunned = False

        self.our_audio_manager = AudioManager()
        self.our_item_list = ItemList()
        self.our_screen_shake = ScreenShakeManager()

    def dropExpOrb(self):
        ExpOrb(self.position, self.exp_drop)
        
    def takeDamage(self, dmg):
        self.startDamageIndicator()
        self.health -= self.our_item_list.getArmorChippedDmg((self.health / self.max_health) * 100, dmg)
        self.our_audio_manager.playAudioImpact()
        self.speed = self.max_speed * self.our_item_list.getMovmentReductionPercent()
        self.stunChance()
        if self.health < 0.001 and not self.is_currently_dying:
            self.is_currently_dying = True
            self.kill()
            return True
        return False

    def startDamageIndicator(self):
        self.is_damage_indicated = True
        self.current_damage_indicator_time = 0

    def stunChance(self):
        if self.our_item_list.isStunEnemy():
            self.stun_duration = self.our_item_list.getStunDuration()
            self.is_stunned = True
    
    def stunLogic(self, delta_time):
        self.stun_duration -= delta_time
        if self.stun_duration <= 0 and self.is_stunned:
            self.is_stunned = False
            self.speed = self.max_speed
        elif self.is_stunned:
            self.speed = 0



    def kill(self):
        r = abs(self.my_OG_color[0] - PARTICLE_ON_DEATH_COLOR_ADJUSTMENT)
        g = abs(self.my_OG_color[1] - PARTICLE_ON_DEATH_COLOR_ADJUSTMENT)
        b = abs(self.my_OG_color[2] - PARTICLE_ON_DEATH_COLOR_ADJUSTMENT)
        ParticleManager.on_death(ParticleManager(), self.position, (r,g,b),self.radius/2)
        self.dropExpOrb()

        if self.our_item_list.canISpawnDudExpo():
            Explode(self.position, self.our_item_list.getDudExploRadius(), self.our_item_list.getDudExploDmg(), self)

        self.our_screen_shake.shakeScreen(3,0.1)
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
        self.stunLogic(delta_time)
        pass

    #for setting a path to a target locaition
    def pathing(self, target: pygame.Vector2, delta_time):
        pass