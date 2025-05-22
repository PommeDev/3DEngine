from Utils.Image.Perspective import *
from Utils.Vector import Vector2D
from Utils.Vector import Vector3D
from Utils.Figure.Vertex import Vertex
import numba as nb
import pygame as p
import Utils.Lights.Ambient as LA
from Utils.Lights.model import diffuse_light_lambert

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
        if not(self.is_ccw()):
            self.P2,self.P3 = self.P3,self.P2
        N = (self.P2 - self.P1).cross(self.P3 - self.P1)  # normale orientée
        L = self.P1 - camera_pos          # vecteur vers la caméra

        return N@L < 0  # True si triangle orienté vers la caméra
    
    def should_draw_2(self,camera_pos,theta):
        if not(self.is_ccw()):
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
        self.normal = np.cross(self.P2.pos.to_array() - self.P1.pos.to_array(),self.P3.pos.to_array()-self.P1.pos.to_array())
        self.normal = np.array(self.normal, dtype=np.float64)
        # Position caméra dans l’espace caméra (c’est 0 si la caméra est au centre)
        camera_in_view = view @ camera_pos.to_array()
        L = V0 - camera_in_view
        if self.bot:
            return not(N.dot(L) < 0)
        
        return N.dot(L) < 0


    def is_ccw(self):
        p1 = Vector2D.Vector2D.from_list(self.P2D[1])
        p0 = Vector2D.Vector2D.from_list(self.P2D[0])
        p2 = Vector2D.Vector2D.from_list(self.P2D[2])
        return ((p1.x - p0.x)*(p2.y - p0.y) - (p1.y - p0.y)*(p2.x - p0.x) > 0)
    

    @nb.njit
    def draw_uv_nb(tampon_SSAA,texture,points_to_fill,p1,p2,p3,uv1,uv2,uv3):
        twidth,theight = texture.shape[0],texture.shape[1]
        for i in range(0,len(points_to_fill),2):
            y,x = points_to_fill[i],points_to_fill[i+1]
            x_u,y_u = uv_barycentre_nb(p1,p2,p3,uv1,uv2,uv3,np.array([x,y]))
            tampon_SSAA[y,x] = texture[int(x_u*twidth),int(y_u*theight)]


    @nb.njit
    def add_light_nb(tampon_SSAA,points_to_fill,lx,ly,lz,intensity_l,light_l,n,P1x,P1y,P1z,spot_pos,spot_dir,cutoff_cos,spot_l,spot_i):
        for i in range(0,len(points_to_fill),2):
            y,x = points_to_fill[i],points_to_fill[i+1]
            color = tampon_SSAA[y,x]
            ambient = compute_ambient_lambert(lx,ly,lz,P1x,P1y,P1z,intensity_l,n,color,light_l)
            spot = spotlight_lighting(np.array([P1x,P1y,P1z],dtype=np.float64),n,spot_pos,spot_dir,cutoff_cos,spot_i,color,spot_l)
 
            tampon_SSAA[y,x] =  ambient + spot



    def draw_uv(self,tampon,ambient:LA.Ambient,spot):
        if not(self.texture is None):
            p1,p2,p3 = self.P2D
            uv1 = self.P1.uv
            uv2 = self.P2.uv
            uv3 = self.P3.uv
            points_to_fill = tampon.fill_triangle_uv(self)
            Triangle.draw_uv_nb(tampon.tampon_SSAA,self.texture,points_to_fill,p1,p2,p3,uv1.to_array(),uv2.to_array(),uv3.to_array())
            
            lx,ly,lz = ambient.pos.to_array()
            Triangle.add_light_nb(tampon.tampon_SSAA,points_to_fill,lx,ly,lz,ambient.intensity,ambient.light,self.normal,self.P1.pos.x,self.P1.pos.y,self.P1.pos.z,spot.pos,spot.direction,spot.cutoff,spot.light,spot.intensity)
        else:
            self.draw_tampon_full(tampon)


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

@nb.njit
def compute_ambient_lambert(x,yy,z,a,b,c,intensity,n,color,light):
    color = color.astype(np.float64) / 255.0
    light = light.astype(np.float64) / 255.0

    pos = np.array([x, yy, z], dtype=np.float64)
    light_pos = np.array([a, b, c], dtype=np.float64)

    L = pos - light_pos
    L = L / np.linalg.norm(L)

    n = n / np.linalg.norm(n)

    diffuse = max(np.dot(L, n), 0.0)
    
    # Calcul lumière (résultat entre 0 et 1)
    result = color * intensity + diffuse * light

    # Remettre en [0–255] et clamp
    result = np.clip(result * 255.0, 0, 255)

    return result
    
@nb.njit
def spotlight_lighting(point, normal, spot_pos, spot_dir, cutoff_cos, intensity, color, light_color):
    L = np.empty(3, dtype=np.float64)
    for i in range(3):
        L[i] = spot_pos[i] - point[i]
    distance = np.sqrt(L[0]**2 + L[1]**2 + L[2]**2)
    if distance == 0.0:
        return color

    for i in range(3):
        L[i] /= distance

    cos_angle = 0.0
    for i in range(3):
        cos_angle += -L[i] * spot_dir[i]

    result = np.empty(3, dtype=np.float64)

    # Normalisation du vecteur normal
    n_len = np.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
    n = np.empty(3, dtype=np.float64)
    for i in range(3):
        n[i] = normal[i] / n_len

    # color et light_color supposés déjà dans [0, 255] (uint8), donc convertis en float ici
    color_f = np.empty(3, dtype=np.float64)
    light_color_f = np.empty(3, dtype=np.float64)
    for i in range(3):
        color_f[i] = color[i] / 255.0
        light_color_f[i] = light_color[i] / 255.0

    a = 1
    b = 0.09
    c = 0.032
    d = distance
    light_color_f /= a+b*d+c*d**2
    if cos_angle >= cutoff_cos:
        spot_effect = cos_angle * cos_angle
        diffuse = 0.0
        for i in range(3):
            diffuse += L[i] * n[i]

        if diffuse < 0.0:
            diffuse = 0.0

        for i in range(3):
            result[i] = (color_f[i] * intensity + diffuse * spot_effect * light_color_f[i]) * 255.0
    else:
        for i in range(3):
            result[i] = (color_f[i] * intensity) * 255.0

    # Clip entre 0 et 255, puis convertir en uint8
    out = np.empty(3, dtype=np.uint8)
    for i in range(3):
        if result[i] > 255.0:
            out[i] = 255
        elif result[i] < 0.0:
            out[i] = 0
        else:
            out[i] = np.uint8(result[i])
    return out