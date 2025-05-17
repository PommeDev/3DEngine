import math
import numpy as np

class Vector3D:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self,other):
        return Vector3D(self.x - other.x, self.y - other.y,self.z - other.z)

    def __mul__(self, other):
        return Vector3D(self.x * other, self.y * other, self.z * other)


    def __truediv__(self,other):
        return Vector3D(self.x / other, self.y / other, self.z/other)
        

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self,other):
        return self.__sub__(other)

    def __rmul__(self, other):
        return self.__mul__(other)


    def __rtruediv__(self,other):
        return self.__truediv__(other)
        


    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self
    
    def __isub__(self,other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        self.z *= other
        return self

    def __itruediv__(self,other):
        self.x /= other
        self.y /= other
        self.z /= other
        return self


    def __matmul__(self,other):
        return self.x*other.x + self.y*other.y + self.z*other.z
    
    def __getitem__(self, idx):
        assert idx == 0 or idx == 1 or idx == 2
        if idx == 0:
            return self.x
        elif idx == 1:
            return self.y
        else:
            return self.z
        
    def __setitem__(self,idx,value):
        assert idx == 0 or idx == 1 or idx == 2
        if idx == 0:
            self.x = value
        elif idx == 1:
            self.y = value
        else:
            self.z = value

    def __len__(self):
        return 3
    
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
    
    def __repr__(self):
        return f"({self.x}, {self.y},{self.z})"
    
    def norme(self):
        return math.sqrt(self.x**2+self.y**2+self.z**2)

    def normalize(self):
        a = self.norme()
        if not(a == 0):
            self.x /= a
            self.y /= a
            self.z /= a

    def __abs__(self):
        return self.norme()

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __eq__(self,other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __neq__(self,other):
        return not(self.__eq__(other))
    
    def to_array(self):
        return np.array([self.x,self.y,self.z])
    
    def from_list(list):
        return Vector3D(list[0],list[1],list[2])