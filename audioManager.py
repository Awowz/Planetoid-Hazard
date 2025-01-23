import pygame

class AudioManager():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AudioManager, cls).__new__(cls)
            cls._instance.init_audio()
        return cls._instance
    
    def init_audio(self):
        pygame.mixer.init()
        self.gunSound = pygame.mixer.Sound("Assets/Audio/laser-gun.ogg")

    def playAudioGunShot(self):
        self.gunSound.play()