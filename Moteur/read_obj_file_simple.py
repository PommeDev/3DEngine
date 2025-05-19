import Utils.Vector.Vector3D as V
import Utils.Figure.Cube as C

def read(file):
    vectors = []
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
    
    #vectors[1], vectors[0] = vectors[0],vectors[1] #pour un rendu plus ocrrect en attendant les Zorders
    return vectors


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


def generate_cubes(vectors):
    c_l = []
    
    for i in vectors:
        c_l.append(C.Cube.from_list(i))
    return c_l

