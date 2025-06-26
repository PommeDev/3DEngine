import numpy as np


class Spot:
    def __init__(self,pos,color = np.array([1.,0.5,1.])):
        self.pos = pos
        self.color = color
