from Utils.Figure.Triangle import Triangle
from Utils.Image.Perspective import *

class Shape:
    def __init__(self, list_triangle):
        self.triangles = list_triangle

        self.zorder = {}
        self.k = self.zorder.keys()
        self.k = sorted(self.k,reverse=True)
    

    def updateZorder(self):
        j = 0
        for i in self.triangles:
            P1 = i.P1
            P2 = i.P2
            P3 = i.P3
            indice = min(P1[2],P2[2],P3[2])
            if self.zorder.get(indice):
                self.zorder[indice].append(j)
            else:
                self.zorder[indice] = [j]
            j += 1
        
        self.k = self.zorder.keys()
        self.k = sorted(self.k,reverse=True)


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

        for i in self.k:
            for l in self.zorder[i]:
                t = self.triangles[l]
                if t.should_draw_2(camera,theta):
                    t.draw_tampon_full(tampon)
                    t.draw_tampon_border(tampon)
        
    

