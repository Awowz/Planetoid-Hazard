import pygame
import random
from constants import *
#from asteroid import Asteroid
from asteroidEnemy import AsteroidEnemy
from meleeEnemy import MeleeEnemy
from itemsList import ItemList
from chestObject import Chest
enemy_types = ["asteroid", "melee"]

class GameDirector(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1,0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.total_time_spent = 0
        self.tower_remaining_time = TOWER_TIMER_LENGTH
        self.current_dificulty = 0
        self.time_passed_till_enemy_spawn = 0
        self.our_item_list = ItemList()

    def __getScreenSpawnCap(self):
        return GAME_DIRECTOR_SCREEN_SPAWN_CAP + ((GAME_DIRECTOR_SCREEN_SPAWN_CAP * self.current_dificulty ) // GAME_DIRECTOR_SCREEN_SPAWN_DIVIDING_FACTOR)
    
    def __totalingUpTime(self, delta_time):
        self.total_time_spent += delta_time
        self.tower_remaining_time -= delta_time
        self.time_passed_till_enemy_spawn += delta_time

    def __getEnemySpawnTime(self):
        new_timer = GAME_DIRECTOR_SPAWN_TIMER - ((GAME_DIRECTOR_SPAWN_TIMER * self.current_dificulty) / 10)
        if new_timer <= 0:
            return 0.2
        return new_timer
    
    def spawn(self):
        enemy_variety_options = min(self.current_dificulty, len(enemy_types) - 1)
        if enemy_variety_options == 0:
            selected_enemy = 0
        else:
            selected_enemy = random.randint(0, enemy_variety_options)

        edge = random.choice(self.edges)
        speed = random.randint(40, 100)
        velocity = edge[0]
        velocity = velocity.rotate(random.randint(-30,30))
        position = edge[1](random.uniform(0,1))

        if enemy_types[selected_enemy] == "asteroid":
            kind = random.randint(1, ASTEROID_KINDS)
            asteroid = AsteroidEnemy(position.x, position.y, ASTEROID_MIN_RADIUS * kind, velocity, speed, add_health=self.healthFormula(ASTEROID_BASE_HEALTH), add_exp_drop=self.expFormula(ASTEROID_BASE_EXP_DROP))
        elif enemy_types[selected_enemy] == "melee":
            melee = MeleeEnemy(position.x, position.y, MELEE_RADIUS, pygame.Vector2(0,1), MELEE_SPEED, MELEE_COLOR, self.healthFormula(MELEE_BASE_HEALTH), self.expFormula(MELEE_BASE_EXP_DROP))


    def checkProgress(self, delta_time):
        self.__totalingUpTime(delta_time)
        
        if self.tower_remaining_time <= 0:
            self.tower_remaining_time = TOWER_TIMER_LENGTH
            self.current_dificulty += 1
            self.spawnReward()
            

        if self.__getEnemySpawnTime() <= self.time_passed_till_enemy_spawn:
            self.time_passed_till_enemy_spawn = 0            
            self.spawn()

    def healthFormula(self,base):
        return self.current_dificulty * 5
    
    def expFormula(self,base):
        return self.current_dificulty * (base / 2)

    def spawnReward(self):
        Chest(pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))