import numpy as np

def perspective_compute(a,c,theta,e):
    """
    a -> position de l'objet
    c -> position de la caméra
    theta -> angle d'Euler de la caméra
    e -> position de la surface d'affichage par rapport à c   
    return : b -> Position de a dans le plan 2D   
    """
    m1 = np.zeros((3,3))
    m1[0,0] = 1
    m1[1,1] = np.cos(theta[0])
    m1[1,2] = np.sin(theta[0])
    m1[2,1] = -np.sin(theta[0])
    m1[2,2] = np.cos(theta[0])

    m2 = np.zeros((3,3))
    m2[0,0] = np.cos(theta[1])
    m2[0,2] = -np.sin(theta[1])
    m2[1,1] = 1
    m2[2,0] = np.sin(theta[1])
    m2[2,2] = np.cos(theta[1])

    m3 = np.zeros((3,3))
    m3[0,0] = np.cos(theta[2])
    m3[0,1] = np.sin(theta[2])
    m3[1,0] = -np.sin(theta[2])
    m3[1,2] = np.cos(theta[2])
    m3[2,2] = 1



    d = ((m1@m2)@m3)@(a-c)

    
    aspect_ratio = 800 / 600
    f = e[2]

    x_ndc = (d[0] / d[2]) * f / aspect_ratio
    y_ndc = (d[1] / d[2]) * f
    
    # Transformation  [-1, 1] vers pixels
    x_screen = int((x_ndc + 1) * 0.5 * 800)
    y_screen = int((1 - y_ndc) * 0.5 * 600)  # inversé pour Pygame

    b = np.array([x_screen, y_screen])

    """
    b = np.array([(e[2]/d[2])*d[0]+e[0],(e[2]/d[2])*d[1]+e[1]])
    """
    return b



def e(FOV):
    e_z = 1/np.tan(FOV/2)
    e =  np.zeros(3)
    e[2] = e_z
    return e

