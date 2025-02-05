import sys
import pygame
import math
from ConstantVariables.constants import *
from Scripts.HitBoxObjects.player import Player
from Scripts.HitBoxObjects.EnemyObjects.baseEnemy import BaseEnemy
from Scripts.ManagerScripts.gameDirector import GameDirector
from Scripts.HitBoxObjects.InteractionObjects.shot import Shot
from Scripts.HitBoxObjects.InteractionObjects.particle import Particle
from Scripts.ManagerScripts.weaponType import WeaponType
from Scripts.ManagerScripts.particleManager import ParticleManager
from Scripts.HitBoxObjects.InteractionObjects.expOrb import ExpOrb
from Scripts.HitBoxObjects.InteractionObjects.itemObject import ItemObject
from Scripts.HitBoxObjects.temporaryTextObject import TextObject
from Scripts.HitBoxObjects.InteractionObjects.explode import Explode
from Scripts.ManagerScripts.itemsList import ItemList
from Scripts.ManagerScripts.playerDeathDraw import PlayerDeathDraw
from Scripts.HitBoxObjects.InteractionObjects.missleObject import Missle
from Scripts.HitBoxObjects.InteractionObjects.chestObject import Chest
from Scripts.ManagerScripts.screenShakeManager import ScreenShakeManager
from Scripts.ManagerScripts.displayItems import DisplayItems
from Scripts.HitBoxObjects.mouse import Mouse
from Scripts.ManagerScripts.itemTextBox import ItemTextBox

our_list = ItemList()
our_shake = ScreenShakeManager()
current_game_state = GAME_STATE

def color_transition(my_player):
    center_x = SCREEN_WIDTH / 2
    center_y = SCREEN_HEIGHT / 2
    x_distance = abs(my_player.position.x - center_x)
    y_distance = abs(my_player.position.y - center_y)

    normalize_x = x_distance / center_x
    normalize_y = y_distance / center_y

    normalize_distance = max(normalize_x, normalize_y)

    center_RGB = BACKGROUND_COLOR_DEFAULT
    outer_edges_RGB = (0,0,0)

    r = int(center_RGB[0] + (-center_RGB[0] * normalize_distance))
    g = int(center_RGB[1] + (-center_RGB[1] * normalize_distance))
    b = int(center_RGB[2] + (-center_RGB[2] * normalize_distance))

    return (r,g,b)
    

def render_game_objects(screen, drawable, my_player, playerDependentDraw, og_screen):
    screen.fill(color_transition(my_player))

    for draw_object in drawable:
        draw_object.draw(screen)

    for draw_object_near_player in playerDependentDraw:
        draw_object_near_player.playerDependentDraw(screen, my_player)

    our_shake.drawScreenShake(screen,og_screen)
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
            if my_player.canIKillPlayer():
                print("GAME OVER!")
                #sys.exit()
                PlayerDeathDraw(my_player.position)
            else:
                single_enemy.kill()
                pass
            
        for single_shot in shots:
            if single_shot.checkCollision(single_enemy):
                has_single_enemy_died = single_enemy.takeDamage(single_shot.damage)#my_player.current_weapon.getDamage())
                if has_single_enemy_died:
                    my_player.setShieldActive()
                ##item checks
                if our_list.canISpawnExpo():
                    Explode(single_shot.position, our_list.getGunPowderAOE(), my_player.current_weapon.shot_damage, single_enemy)
                if our_list.canISpawnMissle():
                    Missle(my_player.position, our_list.getMissleDmg())
                #single_shot.kill()
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


    our_shake.update(delta_time)

def pause_update(delta_time, my_mouse, my_item_text_box, pause_updateable, pause_item):
    for update_object in pause_updateable:
        update_object.pauseUpdate(delta_time)
    
    is_item_being_highlighted = False
    for single_pickup in pause_item:
        if my_mouse.checkCollision(single_pickup):
            is_item_being_highlighted = True
            my_item_text_box.setIsVisable(single_pickup.my_item_str, single_pickup.item_desct)
        elif not is_item_being_highlighted:
            my_item_text_box.setNotVisable()

def pause_draw(screen, og_screen, display_all_items, pause_drawable):
    screen.fill(pygame.color.Color(BACKGROUND_COLOR_DEFAULT))
    pause_text = pygame.font.Font(None, PLAYER_DEATH_UI_FONT).render("GAME PAUSED", True, UI_FONT_COLOR)
    esc_text = pygame.font.Font(None, UI_FONT_SIZE).render("ESC to resume", True, UI_FONT_COLOR)
    screen.blit(pause_text, pygame.Vector2((SCREEN_WIDTH / PAUSE_TEXT_X_OFFSET), (SCREEN_HEIGHT / PAUSE_TEXT_Y_OFFSET)))
    screen.blit(esc_text, pygame.Vector2((SCREEN_WIDTH / PAUSE_ESC_TEXT_X_OFFSET), (SCREEN_HEIGHT / PAUSE_ESC_TEXT_Y_OFFSET)))

    for draw_object in pause_drawable:
        draw_object.pauseDraw(screen)

    display_all_items.draw(screen)

    og_screen.blit(screen, (0,0))
    pygame.display.flip()

def reward_draw(screen, og_screen, reward_drawable):
    for draw_object in reward_drawable:
        draw_object.draw(screen) 
        og_screen.blit(screen, (0,0))
        pygame.display.flip()

def reward_update(delta_time, my_mouse, my_item_text_box, reward_updateable, reward_item, reward_chest):
    for update_object in reward_updateable:
        update_object.update(delta_time)

    is_item_being_highlighted = False
    for single_pickup in reward_item:
        if my_mouse.checkCollision(single_pickup):
            is_item_being_highlighted = True
            my_item_text_box.setIsVisable(single_pickup.my_item_str, single_pickup.item_desct)
            if pygame.mouse.get_pressed(3)[0]:
                single_pickup.givePlayerItem()
                for chest in reward_chest:
                    chest.kill()
                global current_game_state
                current_game_state = GAME_STATE
        elif not is_item_being_highlighted:
            my_item_text_box.setNotVisable()

def main():
    pygame.init()
    clock_object = pygame.time.Clock()
    delta_time = 0 ## amount of time passed since last frame was drawn
    og_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen = og_screen.copy()
  
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
    pause_drawable = pygame.sprite.Group()
    pause_updateable = pygame.sprite.Group()
    pause_item = pygame.sprite.Group()
    reward_updateable = pygame.sprite.Group()
    reward_drawable = pygame.sprite.Group()
    reward_item = pygame.sprite.Group()
    reward_chest = pygame.sprite.Group()

    # note: must be created after asigning static field, otherwise existing object wont take effect
    WeaponType.containers =     (updatable, drawable, playerDependentDraw)
    Player.containers =         (updatable, drawable)
    BaseEnemy.containers =      (updatable, all_enemies, drawable, pathing)
    GameDirector.containers =   (checkProgress, drawable)
    Shot.containers =           (updatable, shots, drawable)
    Particle.containers =       (updatable, drawable)
    ExpOrb.containers =         (updatable, drawable, all_exp, all_pickup)
    ItemObject.containers =     (updatable, drawable, all_pickup, pause_item, reward_drawable, reward_updateable, reward_item) #add 'allexp'
    TextObject.containers =     (updatable, drawable)
    Explode.containers =        (updatable, drawable, explode_radius)
    PlayerDeathDraw.containers = (updatable, drawable)
    Missle.containers =         (drawable, shots, all_pathing_missle)
    Chest.containers =          (reward_drawable, reward_updateable, all_pickup, reward_chest)
    Mouse.containers =          (pause_updateable, reward_updateable)
    ItemTextBox.containers =    (pause_drawable, pause_updateable, reward_drawable, reward_updateable)

    my_player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  
    my_game_director = GameDirector()
    my_particle_manager = ParticleManager()
    my_mouse = Mouse()
    my_item_text_box = ItemTextBox()
    action_limitor = ACTION_TIME_LIMIT
    display_all_items = None
    global current_game_state
    

    print("\n\nKEYBINDS:\nW - UP\nA\\D - LEFT AND RIGHT\nS - REVERSE\nE - SWAP WEAPON\nSPACE - SHOOT \nHOLD LSHIFT TO SLOW AIM")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            

        keys = pygame.key.get_pressed()
        action_limitor -= delta_time
        if keys[pygame.K_ESCAPE] and action_limitor <= 0:
            action_limitor = ACTION_TIME_LIMIT
            if current_game_state == GAME_STATE:
                current_game_state = PAUSE_STATE
                display_all_items = DisplayItems()
            else:
                display_all_items.kill()
                del display_all_items
                current_game_state = GAME_STATE
        elif keys[pygame.K_TAB] and action_limitor <= 0 and my_player.areRewardsAvaliable() and current_game_state == GAME_STATE:
            action_limitor = ACTION_TIME_LIMIT
            current_game_state = REWARD_STATE
            my_player.consumeReward()
            Chest(pygame.Vector2(CHEST_X_POS, CHEST_Y_POS))
        



        if current_game_state == PAUSE_STATE:
            pause_update(delta_time, my_mouse, my_item_text_box, pause_updateable, pause_item)
            pause_draw(screen, og_screen, display_all_items, pause_drawable)
        elif current_game_state == GAME_STATE:
            update_game_logic(delta_time, my_player, updatable, all_enemies, shots, checkProgress, my_particle_manager, all_exp, all_pickup, explode_radius, all_pathing_missle)
            render_game_objects(screen, drawable, my_player, playerDependentDraw, og_screen)
        elif current_game_state == REWARD_STATE:
            reward_update(delta_time, my_mouse,my_item_text_box, reward_updateable,reward_item, reward_chest)
            reward_draw(screen, og_screen, reward_drawable)
        

        ##after the main gameloop has run run tick
        delta_time = clock_object.tick(60) / 1000 




if __name__ == "__main__":
    main()