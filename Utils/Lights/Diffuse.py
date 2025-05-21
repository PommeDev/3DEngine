import Utils.Vector.Vector3D as V3
from Utils.Lights.model import *


class Diffuse:
    def __init__(self,pos:V3.Vector3D,c):
        self.pos = pos
        self.color = c

