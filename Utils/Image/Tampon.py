import numpy as np
import pygame as p
import numba as nb

class Tampon:
    def __init__(self, size, indice):
        self.width = size[0]
        self.height = size[1]
        self.indice = indice

        self.tampon = np.zeros((size[0],size[1],3),dtype=np.uint8)
        self.tampon_SSAA = np.zeros((size[0]*2,size[1]*2,3),dtype=np.uint8)


    def __len__(self):
        return self.width*self.height
    

    @nb.njit(parallel=True)
    def downsample_ssaa(src):
        h, w = src.shape[0] // 2, src.shape[1] // 2
        dst = np.empty((h, w, 3), dtype=np.uint8)
        for i in nb.prange(h):
            for j in range(w):
                for k in range(3):
                    v = (
                        src[2*i, 2*j, k] + src[2*i, 2*j+1, k] +
                        src[2*i+1, 2*j, k] + src[2*i+1, 2*j+1, k]
                    ) // 4
                    dst[i, j, k] = v
        return dst

    def SSAA(self):
        self.tampon = Tampon.downsample_ssaa(self.tampon_SSAA)
        

    @nb.njit
    def bresenham_numba(x0, y0, x1, y1):
        max_points = 4096  # taille max (à ajuster si besoin)
        points = np.empty((max_points, 2), dtype=np.int32)
        idx = 0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            points[idx, 0] = x0
            points[idx, 1] = y0
            idx += 1
            if x0 == x1 and y0 == y1 or idx >= max_points:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

        return points[:idx]


    def bresenham(self,P1,P2):
        """Génère les points d'une ligne entre (x0, y0) et (x1, y1) dans un tableau discret"""
        points = []
        x0,y0 = P1[0],P1[1]
        x1,y1 = P2[0],P2[1]

        points = Tampon.bresenham_numba(x0,y0,x1,y1)
        return points

    
    def draw_line(self,P1,P2,c):
        for x, y in self.bresenham(P1,P2):
            if 0 <= y < self.tampon_SSAA.shape[0] and 0 <= x < self.tampon_SSAA.shape[1]:
                self.tampon_SSAA[y, x] = c  


    def blit(self,window):
        self.SSAA()
        surface = p.surfarray.make_surface(self.tampon)
        window.blit(surface, (0, 0))
        self.tampon_SSAA.fill(0)
        return self.indice