import Utils.Vector.Vector3D as V
import Utils.Figure.Cube as C

def read(file):
    #probleme dans l'odre des sommets
    vectors = []
    with open(file,'r') as f:
        t = []
        for line in f.readlines():
            if line[0:2] == 'v ':
                line = line.split(" ")
                t.append(V.Vector3D(float(line[1])*100,float(line[2])*100,float(line[3])*100))
            else:
                if len(t) > 0:
                    vectors.append(t)
                t = []
    
    return vectors



def generate_cubes(vectors):
    c_l = []
    
    for i in vectors:
        c_l.append(C.Cube.from_list(i))
    return c_l

