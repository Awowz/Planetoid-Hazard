import pygame
import random
from particle import Particle
from constants import * 

class ParticleManager():
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.particle_list = []
        self.time_passed = 0

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
        