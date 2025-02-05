import pygame
import pygame.tests
from Scripts.HitBoxObjects.circleshape import CircleShape
from ConstantVariables.constants import *
from Scripts.ManagerScripts.particleManager import ParticleManager
from Scripts.ManagerScripts.weaponType import WeaponType
from Scripts.ManagerScripts.itemsList import ItemList

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.particleManager = ParticleManager()
        self.current_weapon = WeaponType()
        self.current_exp = 0
        self.current_lvl = 1
        self.exp_radius_magnet = PLAYER_EXP_MAGNET
        self.our_items_list = ItemList()
        self.font = pygame.font.Font(None, UI_FONT_SIZE)
        self.player_turn_speed = PLAYER_TURN_SPEED
        self.press_tab_text = self.font.render("TAB", True, UI_FONT_COLOR)

        self.is_player_dead = False
        self.is_shield_active = False
        self.remaining_shield_time = 0

        self.avaliable_rewards = 0

    def getRequiredExp(self):
        return (self.current_lvl / PLAYER_EXP_MULTIPLIER_BASE) ** PLAYER_EXP_MULTIPLIER_EXPO

    def gainExp(self, exp_amount):
        self.current_exp += exp_amount
        if self.current_exp >= self.getRequiredExp():
            self.current_exp = self.current_exp - self.getRequiredExp()
            self.current_lvl += 1
            self.particleManager.confetti(self.position)
            self.avaliable_rewards += 1

    def getPlayerExpRadius(self):
        return self.exp_radius_magnet + self.our_items_list.getMagnetRadius()
    
    def areRewardsAvaliable(self) ->bool:
        if self.avaliable_rewards > 0: return True
        return False
    
    def consumeReward(self):
        self.avaliable_rewards -= 1

    def triangle(self):
        forward = pygame.Vector2(0,1).rotate(self.rotation)
        right = pygame.Vector2(0,1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def __drawXpBar(self, screen):
        pygame.draw.rect(screen, PLAYER_EXP_DISPLAY_BORDER_COLOR, [PLAYER_EXP_DISPLAY_POSITION_X, PLAYER_EXP_DISPLAY_POSITION_Y, PLAYER_EXP_DISPLAY_LENGTH + PLAYER_EXP_DISPLAY_BORDER, PLAYER_EXP_DISPLAY_HEIGHT + PLAYER_EXP_DISPLAY_BORDER], 0)
        normalize_length = (self.current_exp + 0.01) / self.getRequiredExp()
        pygame.draw.rect(screen, EXP_COLOR, [PLAYER_EXP_DISPLAY_POSITION_X, PLAYER_EXP_DISPLAY_POSITION_Y, PLAYER_EXP_DISPLAY_LENGTH * normalize_length, PLAYER_EXP_DISPLAY_HEIGHT])

    def __drawPlayerLvl(self, screen):
        text = self.font.render(f"{self.current_lvl} LVL", True, UI_FONT_COLOR)
        screen.blit(text, pygame.Vector2(PLAYER_EXP_DISPLAY_POSITION_X, PLAYER_EXP_DISPLAY_POSITION_Y - UI_PLAYER_LVL_OFFSET))

    def __drawShield(self, screen):
        if not self.is_shield_active: return
        normalize = self.remaining_shield_time / self.our_items_list.getShieldDurration()

        forward = pygame.Vector2(0,1).rotate(self.rotation) * 2
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius * 1.5

        new_bottom_left = self.position - (forward * self.radius - right) * normalize
        new_bottom_right = self.position - (forward * self.radius + right) * normalize
        new_top_right = self.position + (forward * self.radius - right) * normalize
        new_top_left = self.position + (forward * self.radius + right) * normalize
        pygame.draw.polygon(screen, SHIELD_COLOR, [new_bottom_right, new_bottom_left,new_top_left, new_top_right], 1)
        
    
    def __drawTabPromt(self,screen):
        if self.avaliable_rewards <= 0: return
        pygame.draw.rect(screen, PLAYER_EXP_DISPLAY_BORDER_COLOR, [TAB_BOX_CENTER_X - (TAB_BOX_WIDTH / 2), TAB_BOX_CENTER_Y - (TAB_BOX_HEIGHT / 2), TAB_BOX_WIDTH, TAB_BOX_HEIGHT], 0)
        pygame.draw.rect(screen, EXP_COLOR, [TAB_BOX_CENTER_X - (TAB_BOX_WIDTH / 2), TAB_BOX_CENTER_Y - (TAB_BOX_HEIGHT / 2), TAB_BOX_WIDTH, TAB_BOX_HEIGHT], 3)
        tab_text_rect = self.press_tab_text.get_rect(center=(TAB_BOX_CENTER_X, TAB_BOX_CENTER_Y))
        screen.blit(self.press_tab_text, tab_text_rect)

        

    def draw(self, screen):
        if self.is_player_dead: return

        self.__drawTabPromt(screen)
        self.__drawXpBar(screen)
        self.__drawPlayerLvl(screen)
        pygame.draw.polygon(screen, "yellow", self.triangle(), 0)
        
        self.__drawShield(screen)
        

    def rotate(self, delta_time):
        self.rotation += self.player_turn_speed * delta_time

    def move(self, delta_time):
        forward = pygame.Vector2(0,1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * delta_time
        back_triangle_position = self.position - pygame.Vector2(0,1).rotate(self.rotation) * self.radius
        self.particleManager.create_particle_thrust(back_triangle_position, self.rotation)

    def shoot(self):
        self.current_weapon.shoot(self.position, self.rotation, self.current_lvl)

    def setShieldActive(self):
        if self.our_items_list.getShieldDurration() == 0: return
        self.is_shield_active = True
        self.remaining_shield_time = self.our_items_list.getShieldDurration()

    def reduceShieldTimer(self, delta_time):
        self.remaining_shield_time -= delta_time
        if self.remaining_shield_time <= 0:
            self.is_shield_active = False

    def killShield(self):
        self.is_shield_active = False
        self.remaining_shield_time = 0

    def canIKillPlayer(self):
        if self.is_shield_active:
            self.killShield()
            return False
        self.is_player_dead = True
        return True

    def update(self, delta_time):
        if self.is_player_dead: return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LSHIFT]:
            self.player_turn_speed = PLAYER_TURN_SPEED / 2
        else:
            self.player_turn_speed = PLAYER_TURN_SPEED

        if keys[pygame.K_w]:
            self.move(delta_time)
        if keys[pygame.K_s]:
            self.move(-delta_time)
        if keys[pygame.K_a]:
            self.rotate(-delta_time)
        if keys[pygame.K_d]:
            self.rotate(delta_time)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_e]:
            self.current_weapon.swap_weapon()
        self.reduceShieldTimer(delta_time)