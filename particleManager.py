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


    def create_standard_particle(self, position, quantity, velocity, degree_variance=0):
        for x in range(quantity):
            temp = Particle(position.x, position.y, PARTICLE_RADIUS, 1)
            temp.velocity = velocity.rotate(random.randint(-degree_variance,degree_variance))
            temp.deceleration = -velocity / temp.fade_time

    def create_particle_thrust(self):
        pass