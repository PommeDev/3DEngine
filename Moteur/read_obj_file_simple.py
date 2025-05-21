import Utils.Vector.Vector3D as V
from Utils.Vector.Vector2D import *
import Utils.Figure.Cube as C
import Utils.Figure.Vertex as Ver

def read(file):
    vectors = []
    uv = []
    with open(file,'r') as f:
        t = []
        for line in f.readlines():
            if line[0:2] == 'v ':
                line = line.split(" ")
                t.append(V.Vector3D(float(line[1])*100,float(line[2])*100,float(line[3])*100))
            else:
                if len(t) > 0:
                    vectors.append(sort_vertex(t))
                t = []
        
        u = []
        f.seek(0)
        for line in f.readlines():
            line = line.strip()
            if line.startswith("vt"):
                line = line.split(" ")
                u.append(Vector2D(float(line[1]),float(line[2])))
            else:
                if len(u) > 0:
                    uv.append(sort_vertex(u))
                u = []

    
    #vectors[1], vectors[0] = vectors[0],vectors[1] #pour un rendu plus ocrrect en attendant les Zorders
    return vectors,uv


def sort_vertex(list):
    list2 = []
    list2.append(list[6])
    list2.append(list[3])
    list2.append(list[2])
    list2.append(list[7])
    list2.append(list[4])
    list2.append(list[1])
    list2.append(list[0])
    list2.append(list[5])
    return list2

def generate_vertices(vectors, uv):
    list = []
    for i,j in zip(vectors,uv):
        ll = []
        for k,l in zip(i,j):
            ll.append(Ver.Vertex(k,l))
        list.append(ll)
    return list

def generate_cubes(vertices):
    c_l = []
    
    for i in vertices:
        c_l.append(C.Cube.from_list(i))
    return c_l

