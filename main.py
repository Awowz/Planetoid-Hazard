import sys
import pygame
import math
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from particle import Particle
from weaponType import WeaponType

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

def render_game_objects(screen, drawable, my_player):
    screen.fill(color_transition(my_player))

    for draw_object in drawable:
        draw_object.draw(screen)

    # the following command should be the last line for rendering
    pygame.display.flip()


def update_game_logic(delta_time, my_player, updatable, all_asteroids, shots):
    for update_object in updatable:
        update_object.update(delta_time)

    for single_asteroid in all_asteroids:     #collision check
        if single_asteroid.checkCollision(my_player):
            print("GAME OVER!")
            sys.exit()
        for single_shot in shots:
            if single_shot.checkCollision(single_asteroid):
                single_shot.kill()
                single_asteroid.kill()
    

def main():
    pygame.init()
    clock_object = pygame.time.Clock()
    delta_time = 0 ## amount of time passed since last frame was drawn
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    all_asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # note: must be created after asigning static field, otherwise existing object wont take effect
    WeaponType.containers = (updatable)
    Player.containers = (updatable, drawable)
    Asteroid.containers = (all_asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    Particle.containers = (updatable, drawable)
    

    my_player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  
    AsteroidField_object = AsteroidField()

    print("\n\nKEYBINDS:\nW - UP\nA\D - LEFT AND RIGHT\nS - REVERSE\nE - SWAP WEAPON\nSPACE - SHOOT")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        update_game_logic(delta_time, my_player, updatable, all_asteroids, shots)

        render_game_objects(screen, drawable, my_player)

        ##after the main gameloop has run run tick
        delta_time = clock_object.tick(60) / 1000 
        



if __name__ == "__main__":
    main()