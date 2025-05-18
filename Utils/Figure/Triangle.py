from Utils.Image.Perspective import *
import pygame as p

class Triangle:
    """Sommets dans l'ordre anti-horraire"""
    def __init__(self,P1,P2,P3):
        self.P1 = P1
        self.P2 = P2
        self.P3 = P3
        self.bot = False

        self.P2D = [0,0,0]

    def __iter__(self):
        yield self.P1
        yield self.P2
        yield self.P3

    
    def compute_2D(self,c,theta,e):
        j = 0
        for i in self:
            self.P2D[j] = perspective_compute(i,c,theta,e)
            j+=1
        
    def draw_empty(self,window,c="red"):
        p.draw.line(window,c,self.P2D[0],self.P2D[1])
        p.draw.line(window,c,self.P2D[1],self.P2D[2])
        p.draw.line(window,c,self.P2D[2],self.P2D[0])

    def draw_full(self,window,c="red"):
        p.draw.polygon(window,c,self.P2D)


    def draw_tampon_empty(self,tampon,c=np.array([255,0,0])):
        P1 = self.P2D[0]
        P2 = self.P2D[1]
        P3 = self.P2D[2]
        tampon.draw_line(P1,P2,c)
        tampon.draw_line(P2,P3,c)
        tampon.draw_line(P1,P3,c)



    def should_draw(self, camera_pos):
        if not(self.is_ccw):
            self.P2,self.P3 = self.P3,self.P2
        N = (self.P2 - self.P1).cross(self.P3 - self.P1)  # normale orientée
        L = self.P1 - camera_pos          # vecteur vers la caméra

        return N@L < 0  # True si triangle orienté vers la caméra
    
    def should_draw_2(self,camera_pos,theta):
        if not(self.is_ccw):
            self.P2,self.P3 = self.P3,self.P2
        
        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(theta[0]), np.sin(theta[0])],
            [0, -np.sin(theta[0]), np.cos(theta[0])]
        ])
        
        Ry = np.array([
            [np.cos(theta[1]), 0, -np.sin(theta[1])],
            [0, 1, 0],
            [np.sin(theta[1]), 0, np.cos(theta[1])]
        ])
        
        Rz = np.array([
            [np.cos(theta[2]), np.sin(theta[2]), 0],
            [-np.sin(theta[2]), np.cos(theta[2]), 0],
            [0, 0, 1]
        ])

        view = Rz @ Ry @ Rx  # rotation totale

        # Transforme les sommets du triangle
        V0 = view @ self.P1.to_array()
        V1 = view @ self.P2.to_array()
        V2 = view @ self.P3.to_array()

        # Normale
        N = np.cross(V1 - V0, V2 - V0)

        # Position caméra dans l’espace caméra (c’est 0 si la caméra est au centre)
        camera_in_view = view @ camera_pos.to_array()
        L = V0 - camera_in_view
        if self.bot:
            return not(N.dot(L) < 0)
        
        return N.dot(L) < 0


    def is_ccw(self):
        p1 = self.P2D[1]
        p0 = self.P2D[0]
        p2 = self.P2D[2]
        return (p1.x - p0.x)*(p2.y - p0.y) - (p1.y - p0.y)*(p2.x - p0.x) > 0