from Utils.Image.Perspective import *
import pygame as p

class Triangle:
    """Sommets dans l'ordre anti-horraire"""
    def __init__(self,P1,P2,P3):
        self.P1 = P1
        self.P2 = P2
        self.P3 = P3

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
