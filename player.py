import pygame
import pygame.tests
from circleshape import CircleShape
from constants import *
from particleManager import ParticleManager
from weaponType import WeaponType
from itemsList import ItemList

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

        self.is_player_dead = False

    def getRequiredExp(self):
        return (self.current_lvl / PLAYER_EXP_MULTIPLIER_BASE) ** PLAYER_EXP_MULTIPLIER_EXPO

    def gainExp(self, exp_amount):
        self.current_exp += exp_amount
        if self.current_exp >= self.getRequiredExp():
            self.current_exp = self.current_exp - self.getRequiredExp()
            self.current_lvl += 1
            self.particleManager.confetti(self.position)

    def getPlayerExpRadius(self):
        return self.exp_radius_magnet + self.our_items_list.getMagnetRadius()

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

    def draw(self, screen):
        if self.is_player_dead: return

        pygame.draw.polygon(screen, "yellow", self.triangle(), 0)
        self.__drawXpBar(screen)
        self.__drawPlayerLvl(screen)
        

    def rotate(self, delta_time):
        self.rotation += PLAYER_TURN_SPEED * delta_time

    def move(self, delta_time):
        forward = pygame.Vector2(0,1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * delta_time
        back_triangle_position = self.position - pygame.Vector2(0,1).rotate(self.rotation) * self.radius
        self.particleManager.create_particle_thrust(back_triangle_position, self.rotation)

    def shoot(self):
        self.current_weapon.shoot(self.position, self.rotation, self.current_lvl)

    def killPlayer(self):
        self.is_player_dead = True

    def update(self, delta_time):
        if self.is_player_dead: return

        keys = pygame.key.get_pressed()

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
