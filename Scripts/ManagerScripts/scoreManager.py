import pygame
from ConstantVariables.constants import *

class ScoreManager():
    _instance = None

    def __new__(cls): #singleton pattern
        if cls._instance is None:
            cls._instance = super(ScoreManager, cls).__new__(cls)
            cls._instance.init_values()
        return cls._instance

    def init_values(self):
        self.time_survived = 0
        self.targets_slain = 0
        self.xp_collected = 0
        self.highest_lvl = 0

        self.highscore_time = 0
        self.highscore_slain = 0
        self.highscore_xp = 0
        self.highscore_lvl = 0

    def __setHighScore(self, time, kills, xp, lvl):
        self.highscore_time = float(time)
        self.highscore_slain = float(kills)
        self.highscore_xp = float(xp)
        self.highscore_lvl = float(lvl)

    def readScore(self):
        f = open(SCORE_FILE, "r")
        str = f.read()
        str_array = str.split('\n')
        self.__setHighScore(str_array[0], str_array[1], str_array[2], str_array[3])
        f.close()
        self.__reset()
    
    def writeScore(self):
        f = open(SCORE_FILE, "w")
        f.write(self.outputStr(max(self.time_survived, self.highscore_time), max(self.targets_slain, self.highscore_slain), max(self. xp_collected, self.highscore_xp), max(self.highest_lvl, self.highscore_lvl)))
        f.close()
        self.__reset()
        
    def __reset(self):
        self.time_survived = 0
        self.targets_slain = 0
        self.xp_collected = 0
        self.highest_lvl = 0

    def incrementKill(self):
        self.targets_slain += 1

    def incrementExp(self, xp):
        self.xp_collected += xp

    def incrementLvl(self):
        self.highest_lvl += 1
    
    def incrementTime(self, delta_time):
        self.time_survived += delta_time
    
    def outputStr(self, time_survived, targets_slain, xp_collected, highest_lvl):
        return f"{time_survived:.4f}\n{targets_slain}\n{xp_collected}\n{highest_lvl}"

    def print_all(self):
        print(f"time:{self.time_survived}\ntargets slain:{self.targets_slain}\nxp:{self.xp_collected}\nplayer lvl:{self.highest_lvl}")

    def getHighScore(self):
        return f"{self.highscore_time:.4f}\n{self.highscore_slain}\n{self.highscore_xp}\n{self.highscore_lvl}"

    def getHighScoreList(self) ->list:
        return [f"Longest time lived:  {self.highscore_time:.4f}", f"Most Enemies slain:  {self.highscore_slain}", f"Most XP collected:  {self.highscore_xp}", f"Highest LVL:  {self.highscore_lvl}"]