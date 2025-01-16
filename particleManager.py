import pygame
from particle import Particle
from constants import * 


class ParticleManager():
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.particle_list = []


    def create_standard_particle(self, position, quantity, velocity):
        for x in range(quantity):
            self.particle_list.append(Particle(position.x, position.y, PARTICLE_RADIUS, 5))

    def create_particle_thrust(self):
        pass