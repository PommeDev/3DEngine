import Utils.Vector.Vector3D as V3
from Utils.Lights.model import *

class Ambient:
    def __init__(self,pos:V3.Vector3D,i,c=np.array([255,253,118])):
        self.pos = pos
        self.light = c
        self.intensity = i

    #Pour du flat shading sinon la normale doit être une moyenne de la normale des faces autour
    def compute_ambient_lambert(pos,y,intensity,n,color,light):
        pos  =V3.Vector3D.from_list(pos)
        y = V3.Vector3D.from_list(y)
        L = abs(pos-y)
        return color*intensity + diffuse_light_lambert(L,n)*light
    
    def compute_ambient_lambert_i(self,y,n,color):
        L = (self.pos-y).normalize()
        return color*self.intensity + diffuse_light_lambert(L,n)*self.light
    




