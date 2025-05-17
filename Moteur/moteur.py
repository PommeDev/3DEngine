import pygame as p
import Utils.Image.Tampon as T
from Utils.Vector.Vector3D import Vector3D
from Utils.Vector.Vector2D import Vector2D
from Utils.Image.Perspective import *

class Moteur:
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



        P1 = Vector3D(100,100,10)
        P2 = Vector3D(200,100,10)
        P3 = Vector3D(100,200,10)
        P4 = Vector3D(200,200,10)
        P5 = Vector3D(100,100,110)
        P6 = Vector3D(200,100,110)
        P7 = Vector3D(100,200,110)
        P8 = Vector3D(200,200,110)
        


        self.p1 = perspective_compute(P1.to_array(),self.camera.to_array(),self.orientation_c.to_array(),e(self.FOV))
        self.p2 = perspective_compute(P2.to_array(),self.camera.to_array(),self.orientation_c.to_array(),e(self.FOV))
        self.p3 = perspective_compute(P3.to_array(),self.camera.to_array(),self.orientation_c.to_array(),e(self.FOV))
        self.p4 = perspective_compute(P4.to_array(),self.camera.to_array(),self.orientation_c.to_array(),e(self.FOV))
        self.p5 = perspective_compute(P5.to_array(),self.camera.to_array(),self.orientation_c.to_array(),e(self.FOV))
        self.p6 = perspective_compute(P6.to_array(),self.camera.to_array(),self.orientation_c.to_array(),e(self.FOV))
        self.p7 = perspective_compute(P7.to_array(),self.camera.to_array(),self.orientation_c.to_array(),e(self.FOV))
        self.p8 = perspective_compute(P8.to_array(),self.camera.to_array(),self.orientation_c.to_array(),e(self.FOV))

        print(self.p1,self.p2,self.p3,self.p4,self.p5,self.p6,self.p7,self.p8)
        #self.tampon.tampon_b[p1_2[0], p1_2[1]] = 255
        #self.tampon.tampon_b[p2_2[0], p2_2[1]] = 255
        #self.tampon.tampon_b[p3_2[0], p3_2[1]] = 255

        #print(p1_2,p2_2,p3_2)
        #p.draw.line(self.window, (0, 255, 0), p1_2, p2_2, 1)  # ligne verte entre p1 et p2
        #p.draw.line(self.window, (0, 255, 0), p2_2, p3_2, 1)  # ligne entre p2 et p3
        #p.draw.line(self.window, (255, 0, 0), p3_2, p1_2, 1)  # ligne entre p3 et p1

    def move_cam_arrow(self):
        #Les positions des x et y sont inversé pour la caméra
        speed = 200
        
        pressed = p.key.get_pressed()
        
        if pressed[p.K_UP]:
            print("aa")
            self.camera[0] -= speed*self.dt
        
        if pressed[p.K_DOWN]:
            self.camera[0] += speed*self.dt
        
        if pressed[p.K_LEFT]:
            self.camera[1] -= speed*self.dt
        
        if pressed[p.K_RIGHT]:
            self.camera[1] += speed*self.dt
        

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
            self.orientation_c[1] += dx * sensitivity  # yaw (rotation Y)
            self.orientation_c[0] += dy * sensitivity  # pitch (rotation X)
            



    def compute_points(self):
        P1 = Vector3D(100,100,10)
        P2 = Vector3D(200,100,10)
        P3 = Vector3D(100,200,10)
        P4 = Vector3D(200,200,10)
        P5 = Vector3D(100,100,110)
        P6 = Vector3D(200,100,110)
        P7 = Vector3D(100,200,110)
        P8 = Vector3D(200,200,110)
        
        self.p1 = perspective_compute(P1.to_array(),self.camera.to_array(),self.orientation_c.to_array(),e(self.FOV))
        self.p2 = perspective_compute(P2.to_array(),self.camera.to_array(),self.orientation_c.to_array(),e(self.FOV))
        self.p3 = perspective_compute(P3.to_array(),self.camera.to_array(),self.orientation_c.to_array(),e(self.FOV))
        self.p4 = perspective_compute(P4.to_array(),self.camera.to_array(),self.orientation_c.to_array(),e(self.FOV))
        self.p5 = perspective_compute(P5.to_array(),self.camera.to_array(),self.orientation_c.to_array(),e(self.FOV))
        self.p6 = perspective_compute(P6.to_array(),self.camera.to_array(),self.orientation_c.to_array(),e(self.FOV))
        self.p7 = perspective_compute(P7.to_array(),self.camera.to_array(),self.orientation_c.to_array(),e(self.FOV))
        self.p8 = perspective_compute(P8.to_array(),self.camera.to_array(),self.orientation_c.to_array(),e(self.FOV))
        

    def run(self):
        p.init()
        is_running = True
        self.old_cam_pos = self.camera
        self.old_cam_angle = self.orientation_c
        scroll_speed = 400
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
                
                self.compute_points()
            
            if not(self.old_cam_angle == self.orientation_c):
                self.compute_points()

            if self.tampon.indice != self.last_indice:
                self.last_indice = self.tampon.blit(self.window)

            self.scroll_dir = 0

            "Arriere"
            p.draw.line(self.window,"blue",self.p5,self.p6)
            p.draw.line(self.window,"blue",self.p5,self.p7)
            p.draw.line(self.window,"blue",self.p6,self.p8)
            p.draw.line(self.window,"blue",self.p7,self.p8)
            "Coté"
            p.draw.line(self.window,"green",self.p1,self.p5)
            p.draw.line(self.window,"green",self.p3,self.p7)
            p.draw.line(self.window,"green",self.p4,self.p8)
            p.draw.line(self.window,"green",self.p2,self.p6)

            
            "Avant"
            p.draw.line(self.window,"red",self.p1,self.p2)
            p.draw.line(self.window,"red",self.p1,self.p3)
            p.draw.line(self.window,"red",self.p2,self.p4)
            p.draw.line(self.window,"red",self.p3,self.p4)



            p.display.flip()
            p.time.Clock().tick(60)
            
        p.quit()