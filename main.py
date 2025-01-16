import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from particle import Particle


def main():
    pygame.init()
    clock_object = pygame.time.Clock()
    delta_time = 0 ## amount of time passed since last frame was drawn
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

  
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    all_asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # note: player must be created after asigning static field, otherwise existing object wont take effect
    Player.containers = (updatable, drawable)
    Asteroid.containers = (all_asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    Particle.containers = (updatable, drawable)

    my_player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  
    AsteroidField_object = AsteroidField()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        


        ##update
        #my_player.update(delta_time)
        for update_object in updatable:
            update_object.update(delta_time)

        #collision check
        for single_asteroid in all_asteroids:
            if single_asteroid.checkCollision(my_player):
                print("GAME OVER!")
                sys.exit()

        # RENDER
        # fill screen first
        screen.fill((35,43,43))

        #draw player sometime after fill but not after flip()
        #my_player.draw(screen)
        for draw_object in drawable:
            draw_object.draw(screen)

        # the following command should be the last line for displaying
        pygame.display.flip()


        ##after the main gameloop has run run tick
        delta_time = clock_object.tick(60) / 1000 




if __name__ == "__main__":
    main()