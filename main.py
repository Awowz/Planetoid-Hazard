import pygame
from constants import *


def main():
    pygame.init()
    clock_object = pygame.time.Clock()
    delta_time = 0 ## amount of time passed since last frame was drawn
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        


        # RENDER
        screen.fill((35,43,43))
        # the following command should be the last line for displaying
        pygame.display.flip()


        ##after the main gameloop has run run tick
        delta_time = clock_object.tick(60) / 1000 


if __name__ == "__main__":
    main()