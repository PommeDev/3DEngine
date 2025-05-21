import pygame as p
import Utils.Image.Tampon as T
from Utils.Vector.Vector3D import Vector3D
from Utils.Vector.Vector2D import Vector2D
from Utils.Image.Perspective import *
from Utils.Figure.Cube import Cube
from Utils.Figure.Shape import Shape
from Utils.Figure.Triangle import Triangle
from Moteur.read_obj_file_simple import * 
from Utils.Figure.Vertex import Vertex
from PIL import Image
from random import randint
import Utils.Lights.Ambient as LA

class Moteur:
    #Probleme les x et y sont inversé partout

    def __init__(self,size=(800,600)):
        self.size = size
        self.window = p.display.set_mode(size)
        self.tampon = T.Tampon(size,1)
        self.last_indice = 0
        self.camera = Vector3D(150,0,-500)
        self.FOV = np.radians(60)
        self.orientation_c = Vector3D(np.radians(-10),np.radians(30),np.radians(90))
        #-10,30,90
        
        self.dragging = False
        self.dt = p.time.Clock().tick(60)/1000.0
        self.scroll_dir = 0


        self.c_l = []
        self.s_l = Shape([])

        self.ambient = LA.Ambient(Vector3D(100,100,0),0.05)

        #self.C1 = Cube(Vector3D(100,100,0),100)
        #self.C1.compute_2D(self.camera,self.orientation_c,e(self.FOV))


        #self.C2 = Cube(Vector3D(100,200,0),100)
        #self.C2.compute_2D(self.camera,self.orientation_c,e(self.FOV))


        #self.S1 = Shape(self.C1.to_triangle())
        #self.S1.to_2D(self.camera,self.orientation_c,e(self.FOV))
        #self.S2 = Shape(self.C2.to_triangle())
        #self.S2.to_2D(self.camera,self.orientation_c,e(self.FOV))



        imageRGB = Image.open("texture1.png").convert("RGB") 
        imageData = np.asarray(imageRGB)
        self.A = Triangle(Vertex(Vector3D(200,100,10),Vector2D(0,0)),Vertex(Vector3D(300,100,10),Vector2D(32/32,0)),Vertex(Vector3D(300,200,110),Vector2D(32/32,32/32)))
        self.A.compute_2D(self.camera,self.orientation_c,e_compute(self.FOV))
        self.A.texture = imageData

    def generate_cubes(self,file):
        pos,u = read(file)
        vertices = generate_vertices(pos,u)
        self.c_l = generate_cubes(vertices)
        
        for i in self.c_l:
            for j in i.to_triangle():
                self.s_l.triangles.append(j)
        

        self.s_l.updateZorder()

        
        for i in self.s_l.triangles:
            i.color = np.array([randint(0,255),randint(0,255),randint(0,255)])
            i.line_color = np.array([randint(0,255),randint(0,255),randint(0,255)])


    def update_cubes(self):
        self.s_l.to_2D(self.camera,self.orientation_c,e_compute(self.FOV))

    def draw_cubes(self):
            self.s_l.draw_uv(self.tampon,self.camera,self.orientation_c,self.ambient)


    def move_cam_arrow(self):
        #Les positions des x et y sont inversé pour la caméra
        speed = 200
        
        pressed = p.key.get_pressed()
        if pressed[p.K_UP]:
            
            self.camera[1] -= speed*self.dt
        
        if pressed[p.K_DOWN]:
            self.camera[1] += speed*self.dt
        
        if pressed[p.K_LEFT]:
            self.camera[0] -= speed*self.dt
        
        if pressed[p.K_RIGHT]:
            self.camera[0] += speed*self.dt
        

    def move_cam(self, event):
        
        if event.type == p.MOUSEWHEEL:
            self.scroll_dir = event.y


    def angle_cam(self,event):
        sensitivity = 0.005
        
        if event.type == p.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                self.dragging = True

        # Quand on relâche le clic gauche
        elif event.type == p.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        # Mouvement souris
        elif event.type == p.MOUSEMOTION and self.dragging:
            dx, dy = event.rel  # Mouvement relatif de la souris
            self.orientation_c[0] += dx * sensitivity  # yaw (rotation Y)
            self.orientation_c[1] += dy * sensitivity  # pitch (rotation X)
            


    def run(self):
        p.init()

        is_running = True
        self.old_cam_pos = self.camera
        self.old_cam_angle = self.orientation_c
        scroll_speed = 400
        self.generate_cubes("TestMyEngine.obj")
        self.update_cubes()
        
        self.A.should_draw_2(self.camera,self.orientation_c)

        while is_running:
            for event in p.event.get():
                if event.type == p.QUIT:
                    is_running = False
                
                self.old_cam_pos = Vector3D(self.camera.x,self.camera.y,self.camera.z)
                self.old_cam_angle = Vector3D(self.orientation_c[0],self.orientation_c[1],self.orientation_c[2])
                self.move_cam(event)
                self.angle_cam(event)

            self.move_cam_arrow()
            self.camera[2] += self.scroll_dir*scroll_speed*self.dt

            if not(is_running):
                break
            
            self.window.fill((0,0,0))

            if not(self.old_cam_pos == self.camera):
                #self.C1.compute_2D(self.camera,self.orientation_c,e(self.FOV))
                #self.C2.compute_2D(self.camera,self.orientation_c,e(self.FOV))
                #self.S1.to_2D(self.camera,self.orientation_c,e(self.FOV))
                #self.S2.to_2D(self.camera,self.orientation_c,e(self.FOV))
                self.update_cubes()
                self.A.compute_2D(self.camera,self.orientation_c,e_compute(self.FOV))
                self.A.should_draw_2(self.camera,self.orientation_c)

            if not(self.old_cam_angle == self.orientation_c):
                #self.C1.compute_2D(self.camera,self.orientation_c,e(self.FOV))
                #self.C2.compute_2D(self.camera,self.orientation_c,e(self.FOV))
                #self.S1.to_2D(self.camera,self.orientation_c,e(self.FOV))
                #self.S2.to_2D(self.camera,self.orientation_c,e(self.FOV))
                self.update_cubes()
                self.A.compute_2D(self.camera,self.orientation_c,e_compute(self.FOV))
                self.A.should_draw_2(self.camera,self.orientation_c)
            
            self.scroll_dir = 0

            #self.C2.draw_empty(self.window)
            #self.C1.draw_empty(self.window)
            #self.S1.draw(self.window,self.camera,self.orientation_c)
            #self.S1.draw_tampon(self.tampon,self.camera,self.orientation_c)
            #self.S2.draw_tampon(self.tampon,self.camera,self.orientation_c)

            self.draw_cubes()
            #self.A.draw_uv(self.tampon,self.ambient)
            self.tampon.blit(self.window)

            p.display.flip()
            p.time.Clock().tick(60)
            
        p.quit()
