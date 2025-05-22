import numpy as np


class Spot:
    def __init__(self,pos,direction,cutoff,Intensity = 0.5,light = np.array([255,255,255])):
        self.pos = pos
        self.direction = direction
        self.cutoff = cutoff
        self.intensity = Intensity
        self.light = light
