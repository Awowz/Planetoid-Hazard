import sys
import pygame
import math
from constants import *
from player import Player
from baseEnemy import BaseEnemy
from gameDirector import GameDirector
from shot import Shot
from particle import Particle
from weaponType import WeaponType
from particleManager import ParticleManager
from expOrb import ExpOrb
from itemObject import ItemObject
from temporaryTextObject import TextObject
from explode import Explode
from itemsList import ItemList
from playerDeathDraw import PlayerDeathDraw
from missleObject import Missle

our_list = ItemList()

def color_transition(my_player):
    center_x = SCREEN_WIDTH / 2
    center_y = SCREEN_HEIGHT / 2
    x_distance = abs(my_player.position.x - center_x)
    y_distance = abs(my_player.position.y - center_y)

    normalize_x = x_distance / center_x
    normalize_y = y_distance / center_y

    normalize_distance = max(normalize_x, normalize_y)

    center_RGB = (35,43,43)
    outer_edges_RGB = (0,0,0)

    r = int(center_RGB[0] + (-center_RGB[0] * normalize_distance))
    g = int(center_RGB[1] + (-center_RGB[1] * normalize_distance))
    b = int(center_RGB[2] + (-center_RGB[2] * normalize_distance))

    return (r,g,b)
    

def render_game_objects(screen, drawable, my_player, playerDependentDraw):
    screen.fill(color_transition(my_player))

    for draw_object in drawable:
        draw_object.draw(screen)

    for draw_object_near_player in playerDependentDraw:
        draw_object_near_player.playerDependentDraw(screen, my_player)

    # the following command should be the last line for rendering
    pygame.display.flip()


def update_game_logic(delta_time, my_player, updatable, all_enemies, shots, checkProgress, my_particle_manager, all_exp, all_pickup, explode_radius, all_pathing_missle):
    for check_progress in checkProgress:
        check_progress.checkProgress(delta_time)

    for update_object in updatable:
        update_object.update(delta_time)

    for single_enemy in all_enemies:     #collision check
        single_enemy.pathing(my_player.position, delta_time)
        if single_enemy.checkCollision(my_player) and not my_player.is_player_dead:
            print("GAME OVER!")
            #sys.exit()
            PlayerDeathDraw(my_player.position)
            my_player.killPlayer()
        for single_shot in shots:
            if single_shot.checkCollision(single_enemy):
                single_enemy.takeDamage(single_shot.damage)#my_player.current_weapon.getDamage())
                
                ##item checks
                if our_list.canISpawnExpo():
                    Explode(single_shot.position, our_list.getGunPowderAOE(), my_player.current_weapon.shot_damage, single_enemy)
                if our_list.canISpawnMissle():
                    Missle(my_player.position, our_list.getMissleDmg())
                single_shot.kill()
                my_particle_manager.on_hit(single_shot.position, single_shot.velocity, particle_radius=(math.ceil(my_player.current_weapon.shot_radius / 2)))
        for expo in explode_radius:
            if expo.checkCollision(single_enemy) and not expo.isTargetAlreadyTakenDamage(single_enemy):
                single_enemy.takeDamage(expo.damage)

    for single_pickup in all_pickup:
        single_pickup.checkCollision(my_player)

    for single_exp in all_exp:
        single_exp.move_to_player(my_player, delta_time)
        
    for singe_missle in all_pathing_missle:
        if len(all_enemies) != 0:
            singe_missle.pathing(all_enemies.sprites()[0].position,delta_time)
    

def main():
    pygame.init()
    clock_object = pygame.time.Clock()
    delta_time = 0 ## amount of time passed since last frame was drawn
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    playerDependentDraw = pygame.sprite.Group()
    all_enemies = pygame.sprite.Group()
    pathing = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    checkProgress = pygame.sprite.Group()
    all_exp = pygame.sprite.Group()
    all_pickup = pygame.sprite.Group()
    explode_radius = pygame.sprite.Group()
    all_pathing_missle = pygame.sprite.Group()

    # note: must be created after asigning static field, otherwise existing object wont take effect
    WeaponType.containers = (updatable, drawable, playerDependentDraw)
    Player.containers = (updatable, drawable)
    BaseEnemy.containers = (all_enemies, updatable, drawable, pathing)
    GameDirector.containers = (checkProgress)
    Shot.containers = (shots, updatable, drawable)
    Particle.containers = (updatable, drawable)
    ExpOrb.containers = (updatable, drawable, all_exp, all_pickup)
    ItemObject.containers = (updatable, drawable, all_pickup) #add 'allexp'
    TextObject.containers = (updatable, drawable)
    Explode.containers = (drawable, explode_radius, updatable)
    PlayerDeathDraw.containers = (drawable, updatable)
    Missle.containers = (drawable, shots, all_pathing_missle)

    my_player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  
    my_game_director = GameDirector()
    my_particle_manager = ParticleManager()

    print("\n\nKEYBINDS:\nW - UP\nA\\D - LEFT AND RIGHT\nS - REVERSE\nE - SWAP WEAPON\nSPACE - SHOOT")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        update_game_logic(delta_time, my_player, updatable, all_enemies, shots, checkProgress, my_particle_manager, all_exp, all_pickup, explode_radius, all_pathing_missle)

        render_game_objects(screen, drawable, my_player, playerDependentDraw)

        ##after the main gameloop has run run tick
        delta_time = clock_object.tick(60) / 1000 
        



if __name__ == "__main__":
    main()