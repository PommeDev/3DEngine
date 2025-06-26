import Utils.Vector.Vector3D as V3
from Utils.Lights.model import *

class Ambient:
    def __init__(self,intensity=0.08,color=np.array([1.,1.,1.])):
        self.color = color
        self.intensity = intensity




