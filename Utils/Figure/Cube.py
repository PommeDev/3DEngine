from Utils.Vector.Vector3D import *
from Utils.Image.Perspective import *
from Utils.Vector.Vector2D import *
import pygame as p
from Utils.Figure.Triangle import Triangle
from Utils.Figure.Vertex import Vertex

class Cube:
    def __init__(self, pos:Vector3D, edge:int):
        x, y, z = pos[0],pos[1],pos[2]
        self.P1 = Vertex(pos)
        self.P2 = Vertex(Vector3D(x+edge,y,z))
        self.P3 = Vertex(Vector3D(x+edge,y-edge,z))
        self.P4 = Vertex(Vector3D(x,y-edge,z))
        self.P5 = Vertex(Vector3D(x,y,z+edge))
        self.P6 = Vertex(Vector3D(x+edge,y,z+edge))
        self.P7 = Vertex(Vector3D(x+edge,y-edge,z+edge))
        self.P8 = Vertex(Vector3D(x,y-edge,z+edge))
        self.all_points = [self.P1,self.P2,self.P3,self.P4,self.P5,self.P6,self.P7,self.P8]
        
        self.p1 = None
        self.p2 = None
        self.p3 = None
        self.p4 = None
        self.p5 = None
        self.p6 = None
        self.p7 = None
        self.p8 = None

        self.all_points_2D = [self.p1,self.p2,self.p3,self.p4,self.p5,self.p6,self.p7,self.p8]

        self.facef = [self.p1,self.p2,self.p3,self.p4]
        self.faceb = [self.p5,self.p6,self.p7,self.p8]
        self.facel = [self.p1,self.p4,self.p5,self.p8]
        self.facer = [self.p2,self.p3,self.p6,self.p7]
        self.faceu = [self.p4,self.p8,self.p7,self.p3]
        self.faced = [self.p1,self.p2,self.p6,self.p5]


    def update(self):
        self.all_points = [self.P1,self.P2,self.P3,self.P4,self.P5,self.P6,self.P7,self.P8]
        self.all_points_2D = [self.p1,self.p2,self.p3,self.p4,self.p5,self.p6,self.p7,self.p8]
        self.facef = [self.p1,self.p2,self.p3,self.p4]
        self.faceb = [self.p5,self.p6,self.p7,self.p8]
        self.facel = [self.p1,self.p4,self.p8,self.p5]
        self.facer = [self.p2,self.p3,self.p7,self.p6]
        self.faceu = [self.p4,self.p8,self.p7,self.p3]
        self.faced = [self.p1,self.p2,self.p6,self.p5]


    def compute_2D(self,c,theta,e):
        self.p1 = Vector2D.from_list(perspective_compute(self.P1.pos,c,theta,e))
        self.p2 = Vector2D.from_list(perspective_compute(self.P2.pos,c,theta,e))
        self.p3 = Vector2D.from_list(perspective_compute(self.P3.pos,c,theta,e))
        self.p4 = Vector2D.from_list(perspective_compute(self.P4.pos,c,theta,e))
        self.p5 = Vector2D.from_list(perspective_compute(self.P5.pos,c,theta,e))
        self.p6 = Vector2D.from_list(perspective_compute(self.P6.pos,c,theta,e))
        self.p7 = Vector2D.from_list(perspective_compute(self.P7.pos,c,theta,e))
        self.p8 = Vector2D.from_list(perspective_compute(self.P8.pos,c,theta,e))
        self.update()

    def __iter__(self):
        yield self.P1
        yield self.P2
        yield self.P3
        yield self.P4
        yield self.P5
        yield self.P6
        yield self.P7
        yield self.P8

    def draw_empty(self,window):
        "Arriere"
        p.draw.line(window,"blue",self.p5,self.p6)
        p.draw.line(window,"blue",self.p5,self.p8)
        p.draw.line(window,"blue",self.p6,self.p7)
        p.draw.line(window,"blue",self.p7,self.p8)
        "Coté"
        p.draw.line(window,"green",self.p1,self.p5)
        p.draw.line(window,"green",self.p3,self.p7)
        p.draw.line(window,"green",self.p4,self.p8)
        p.draw.line(window,"green",self.p2,self.p6)

        "Avant"
        p.draw.line(window,"red",self.p1,self.p2)
        p.draw.line(window,"red",self.p2,self.p3)
        p.draw.line(window,"red",self.p1,self.p4)
        p.draw.line(window,"red",self.p3,self.p4)

    def draw_full(self, window):
        p.draw.polygon(window,"blue",self.faceb)
        p.draw.polygon(window,"green",self.faced)
        p.draw.polygon(window,"green",self.facer)
        p.draw.polygon(window,"green",self.facel)
        p.draw.polygon(window,"green",self.faceu)
        p.draw.polygon(window,"red",self.facef)

    def to_triangle(self):
        """
        t1 = Triangle(self.P1,self.P2,self.P4) # O
        t2 = Triangle(self.P2,self.P3,self.P4) # O
        t3 = Triangle(self.P2,self.P6,self.P3) # O
        t4 = Triangle(self.P6,self.P7,self.P3) # O
        t5 = Triangle(self.P6,self.P7,self.P8) # O
        t6 = Triangle(self.P8,self.P5,self.P6) # O
        t7 = Triangle(self.P4,self.P1,self.P8) # O
        t8 = Triangle(self.P1,self.P5,self.P8) # O
        t9 = Triangle(self.P8,self.P3,self.P4) # O
        t10 = Triangle(self.P3,self.P8,self.P7) # O
        t11 = Triangle(self.P1,self.P5,self.P2) # O
        t12 = Triangle(self.P2,self.P5,self.P6) #O
        """
        t1  = Triangle(self.P1, self.P2, self.P3)
        t2  = Triangle(self.P1, self.P3, self.P4)

        t3  = Triangle(self.P5, self.P7, self.P6)
        t4  = Triangle(self.P5, self.P8, self.P7)

        t5  = Triangle(self.P1, self.P4, self.P8)
        t6  = Triangle(self.P1, self.P8, self.P5)

        t7  = Triangle(self.P2, self.P7, self.P6)
        t8  = Triangle(self.P2, self.P3, self.P7)
        t7.bot = True
        t8.bot = True

        t9  = Triangle(self.P4, self.P3, self.P7)
        t10 = Triangle(self.P4, self.P7, self.P8)


        t11 = Triangle(self.P1, self.P5, self.P6)
        t12 = Triangle(self.P1, self.P6, self.P2)
        

        return [t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12]
    
    def from_list(list):
        C = Cube(Vector3D(),0)
        C.P1 = list[0]
        C.P2 = list[1]
        C.P3 = list[2]
        C.P4 = list[3]
        C.P5 = list[4]
        C.P6 = list[5]
        C.P7 = list[6]
        C.P8 = list[7]
        C.update()

        return C