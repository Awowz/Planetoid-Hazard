import pygame
import random
from Scripts.HitBoxObjects.InteractionObjects.particle import Particle
from ConstantVariables.constants import * 

class ParticleManager():
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.particle_list = []
        self.time_passed = 0

    def on_death(self, position, color, death_impact_size=2, particle_radius=1):
        for x in range(45):
            particle_velocity = pygame.Vector2(0,1) * (death_impact_size * PARTICLE_ON_DEATH_SPEED * random.uniform(0.1,1.5))
            self.create_standard_particle(1,position, particle_velocity, particle_radius, degree_variance=360, fade_time=1.5, color=color)

    def explosion(self, position):
        for x in range (9):
            velocity = pygame.Vector2(0,1) * (EXPLOSION_PARTICLE_SPEED * random.uniform(0.01,1.5))
            self.create_standard_particle(1,position, velocity, EXPLOSION_PARTICLE_RADIUS, particle_thickness=EXPLOSION_PARTICLE_THICKNESS, degree_variance=360, fade_time=EXPLOSION_PARTICLE_FADE, color=(255,255,255))

    def confetti(self, position):
        for x in range(70):
            r = random.randint(0,255)
            g = random.randint(0, 255)
            b = random.randint(0,255)
            particle_velocity = pygame.Vector2(0,1) * (CONFETTI_PARTICLE_SPEED * random.uniform(0.06, 2.0))
            self.create_standard_particle(1,position, particle_velocity, 2, degree_variance=360, fade_time=2.2, color=(r,g,b))

    def on_hit(self, position, velocity, particle_radius=1, degree_variance=69):
        self.create_standard_particle(1, position, -velocity, particle_radius, 0, PARTICLE_ON_HIT_FADE, degree_variance, color=(140,140,140))


    def create_standard_particle(self, quantity, position, velocity, particle_radius=PARTICLE_RADIUS, particle_thickness=1, fade_time = 1, degree_variance=0, color=(0,0,255)):
        for x in range(quantity):
            temp = Particle(position.x, position.y, particle_radius, fade_time=fade_time ,thickness=particle_thickness, color=color)
            temp.velocity = velocity.rotate(random.randint(-degree_variance,degree_variance))
            temp.deceleration = -velocity / temp.fade_time

    def create_particle_thrust(self, position, object_rotation):

        velocity = pygame.Vector2(0,1).rotate(object_rotation)
        temp = Particle(position.x, position.y, PARTICLE_RADIUS_TRHUST, random.uniform(0.05,0.4), 0, (255,random.randint(0,233), 0))
        temp.velocity = velocity.rotate(random.randint(-PARTICLE_THRUST_DEGREE_VARIANCE,PARTICLE_THRUST_DEGREE_VARIANCE)) * -PARTICLE_THRUST_SPEED
        