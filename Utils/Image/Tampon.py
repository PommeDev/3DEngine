import numpy as np
import pygame as p

class Tampon:
    def __init__(self, size, indice):
        self.width = size[0]
        self.height = size[1]
        self.indice = indice

        self.tampon_r = np.zeros(size,dtype=np.uint8)
        self.tampon_g = np.zeros(size,dtype=np.uint8)
        self.tampon_b = np.zeros(size,dtype=np.uint8)


    def __len__(self):
        return self.width*self.height
    

    def blit(self,window):
        array = np.dstack((self.tampon_r, self.tampon_g, self.tampon_b))

        surface = p.surfarray.make_surface(array.swapaxes(0, 1))  # Pygame attend (W, H)

        window.blit(surface, (0, 0))
        return self.indice