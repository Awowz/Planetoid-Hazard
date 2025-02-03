import pygame
from ConstantVariables.constants import *

class AudioManager():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AudioManager, cls).__new__(cls)
            cls._instance.init_audio()
        return cls._instance
    
    def init_audio(self):
        pygame.mixer.init()
        self.gunSound = pygame.mixer.Sound(AUDIO_LOCATION_LAZER_GUN)
        self.impact = pygame.mixer.Sound(AUDIO_LOCATION_IMPACT)
        
        self.isMute = True
        self.isMuteAllForSanity()

    def playAudioGunShot(self):
        self.gunSound.play()

    def playAudioImpact(self):
        self.impact.play()

    def isMuteAllForSanity(self):
        if self.isMute:
            self.gunSound.set_volume(0)
            self.impact.set_volume(0)