import random

class ScreenShakeManager():
    _instance = None

    def __new__(cls): #singleton pattern
        if cls._instance is None:
            cls._instance = super(ScreenShakeManager, cls).__new__(cls)
            cls._instance.init_inventory()
        return cls._instance

    def init_inventory(self):
        self.screen_shake_duration = 0
        self.current_intensity = 0

    def update(self, delta_time):
        self.screen_shake_duration -= delta_time
        self.__updateShakeDuration()

    def __updateShakeDuration(self):
        if self.screen_shake_duration <= 0:
            self.current_intensity = 0

    def shakeScreen(self, intensitiy=1, duration=0.01):
        self.current_intensity += intensitiy
        
        self.screen_shake_duration = max(self.screen_shake_duration, duration)
    
    def __shakeLogic(self):
        if self.current_intensity == 0: return (0,0)
        return (random.randint(-self.current_intensity, self.current_intensity), random.randint(-self.current_intensity, self.current_intensity))

    def drawScreenShake(self, screen, og_screen):
         og_screen.blit(screen, self.__shakeLogic())