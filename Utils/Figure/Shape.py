from Utils.Figure.Triangle import Triangle
from Utils.Image.Perspective import *

class Shape:
    def __init__(self, list_triangle,c=np.array([255,0,0]),cl=np.array([0,255,0])):
        self.triangles = list_triangle
        self.color = c
        self.line_color = cl
    
    def to_2D(self,c,theta,e):
        for i in self.triangles:
            i.compute_2D(c,theta,e)

    def draw(self,window,camera,theta):

        c = ["blue","blue","red","red","green","green","white","white","cyan","cyan","yellow","yellow"]
        j = 0
        for i in self.triangles:
            if i.should_draw_2(camera,theta):
                i.draw_empty(window,c[j])
            
            j+= 1
        

    def draw_tampon(self, tampon,camera,theta):
        for i in self.triangles:
            if i.should_draw_2(camera,theta):
                i.draw_tampon_full(tampon,self.color)
                i.draw_tampon_border(tampon,self.line_color)
        
    

