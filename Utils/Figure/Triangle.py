from Utils.Image.Perspective import *
from Utils.Vector import Vector2D
from Utils.Figure.Vertex import Vertex
import numba as nb
import pygame as p


class Triangle:
    """Sommets dans l'ordre anti-horraire"""
    def __init__(self,P1:Vertex,P2:Vertex,P3:Vertex,color=np.array([255,0,0]),line_color=np.array([0,255,0])):
        self.P1 = P1
        self.P2 = P2
        self.P3 = P3
        self.bot = False
        self.color = color
        self.line_color = line_color
        self.P2D = [0,0,0]
        self.texture = None

    def __iter__(self):
        yield self.P1
        yield self.P2
        yield self.P3

    
    def compute_2D(self,c,theta,e):
        j = 0
        for i in self:
            self.P2D[j] = perspective_compute(i.pos,c,theta,e)
            j+=1
        
    def draw_empty(self,window):
        p.draw.line(window,self.color,self.P2D[0],self.P2D[1])
        p.draw.line(window,self.color,self.P2D[1],self.P2D[2])
        p.draw.line(window,self.color,self.P2D[2],self.P2D[0])

    def draw_full(self,window):
        p.draw.polygon(window,self.color,self.P2D)


    def draw_tampon_empty(self,tampon):
        P1 = self.P2D[0]
        P2 = self.P2D[1]
        P3 = self.P2D[2]
        tampon.draw_line(P1,P2,self.line_color)
        tampon.draw_line(P2,P3,self.line_color)
        tampon.draw_line(P1,P3,self.line_color)


    def draw_tampon_border(self,tampon):
        #Bug legerement
        P1 = Vector2D.Vector2D.from_list(self.P2D[0])
        P2 = Vector2D.Vector2D.from_list(self.P2D[1])
        P3 = Vector2D.Vector2D.from_list(self.P2D[2])
        a = abs(P1-P2)
        b = abs(P2-P3)
        d = abs(P1-P3)
        if a >= b and a >= d:
            tampon.draw_line(P2,P3,self.line_color)
            tampon.draw_line(P1,P3,self.line_color)

        elif b >= a and b >= d:
            tampon.draw_line(P1,P2,self.line_color)
            tampon.draw_line(P1,P3,self.line_color)
        else:
            tampon.draw_line(P1,P2,self.line_color)
            tampon.draw_line(P2,P3,self.line_color)
        


    def draw_tampon_full(self,tampon):
        tampon.fill_triangle(self,self.color)


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
        V0 = view @ self.P1.pos.to_array()
        V1 = view @ self.P2.pos.to_array()
        V2 = view @ self.P3.pos.to_array()

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
    

    @nb.njit
    def draw_uv_nb(tampon_SSAA,texture,points_to_fill,p1,p2,p3,uv1,uv2,uv3):
        for i in range(0,len(points_to_fill),2):
            y,x = points_to_fill[i],points_to_fill[i+1]
            x_u,y_u = uv_barycentre_nb(p1,p2,p3,uv1,uv2,uv3,np.array([x,y]))
            tampon_SSAA[y,x] = texture[int(x_u),int(y_u)]

    def draw_uv(self,tampon):
        p1,p2,p3 = self.P2D
        uv1 = self.P1.uv
        uv2 = self.P2.uv
        uv3 = self.P3.uv
        points_to_fill = tampon.fill_triangle_uv(self)
        Triangle.draw_uv_nb(tampon.tampon_SSAA,self.texture,points_to_fill,p1,p2,p3,uv1.to_array(),uv2.to_array(),uv3.to_array())
        


    def uv_barycentre(self,p):
        p1,p2,p3 = self.P2D
        uv1,uv2,uv3 = self.P1.uv,self.P2.uv,self.P3.uv
        x,y = p[0],p[1]
        x1,y1 = p1[0],p1[1]
        x2,y2 = p2[0],p2[1]
        x3,y3 = p3[0],p3[1]
        denom = (y2-y3)*(x1-x3)+(x3-x2)*(y1-y3)
        alpha = ((y2-y3)*(x-x3)+(x3-x2)*(y-y3))/denom
        beta = ((y3-y1)*(x-x3)+(x1-x3)*(y-y3))/denom
        gamma = 1-alpha-beta
        uvp = alpha*uv1+beta*uv2+gamma*uv3
        return uvp


@nb.njit
def uv_barycentre_nb(p1,p2,p3,uv1,uv2,uv3,p):
    x,y = p[0],p[1]
    x1,y1 = p1[0],p1[1]
    x2,y2 = p2[0],p2[1]
    x3,y3 = p3[0],p3[1]
    denom = (y2-y3)*(x1-x3)+(x3-x2)*(y1-y3)
    alpha = ((y2-y3)*(x-x3)+(x3-x2)*(y-y3))/denom
    beta = ((y3-y1)*(x-x3)+(x1-x3)*(y-y3))/denom
    gamma = 1-alpha-beta
    uvp = alpha*uv1+beta*uv2+gamma*uv3
    return uvp