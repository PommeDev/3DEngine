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


    @nb.njit
    def fill_triangle_nb(p1, p2, p3, image, color):
        (x1, y1), (x2, y2), (x3, y3) = sort_vertices_by_y(p1, p2, p3)

        height = y3 - y1
        if height <= 0:
            return

        x_left = np.empty(height, dtype=np.int32)
        x_right = np.empty(height, dtype=np.int32)

        len12 = edge_interpolate(y1, y2, x1, x2, x_left)
        len23 = edge_interpolate(y2, y3, x2, x3, x_left[len12:])
        len13 = edge_interpolate(y1, y3, x1, x3, x_right)

        total = len12 + len23
        if total != len13:
            min_len = min(total, len13)
            x_left = x_left[:min_len]
            x_right = x_right[:min_len]
        else:
            min_len = total

        for i in range(min_len):
            y = y1 + i
            if 0 <= y < image.shape[0]:
                xl = x_left[i]
                xr = x_right[i]
                if xl > xr:
                    xl, xr = xr, xl
                for x in range(xl, xr + 1):
                    if 0 <= x < image.shape[1]:
                        image[y, x] = color


    def fill_triangle(self,triangle,c):
        P1 = triangle.P2D[0]
        P2 = triangle.P2D[1]
        P3 = triangle.P2D[2]
        Tampon.fill_triangle_nb(P1,P2,P3,self.tampon_SSAA,c)


    def blit(self,window):
        self.SSAA()
        surface = p.surfarray.make_surface(self.tampon)
        window.blit(surface, (0, 0))
        self.tampon_SSAA.fill(0)
        return self.indice
    


@nb.njit
def edge_interpolate(y0, y1, x0, x1, result):
    if y0 == y1:
        return 0  # rien à remplir
    length = abs(y1 - y0)
    for i in range(length):
        t = i / length
        x = int(x0 + t * (x1 - x0))
        result[i] = x
    return length

@nb.njit
def sort_vertices_by_y(p1, p2, p3):
    # Trie les sommets par y croissant
    pts = [p1, p2, p3]
    for i in range(3):
        for j in range(i + 1, 3):
            if pts[i][1] > pts[j][1]:
                pts[i], pts[j] = pts[j], pts[i]
    return pts[0], pts[1], pts[2]