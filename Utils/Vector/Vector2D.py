from math import *
import numpy as np

class Vector2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self,other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector2D(self.x * other, self.y * other)


    def __truediv__(self,other):
        return Vector2D(self.x / other, self.y / other)
        

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
        return self
    
    def __isub__(self,other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __itruediv__(self,other):
        self.x /= other
        self.y /= other
        return self


    def __matmul__(self,other):
        return self.x*other.x + self.y*other.y
    
    def __getitem__(self, idx):
        assert idx == 0 or idx == 1
        if idx == 0:
            return self.x
        else:
            return self.y
        
    def __setitem__(self,idx,value):
        assert idx == 0 or idx == 1
        if idx == 0:
            self.x = value
        else:
            self.y = value

    def __len__(self):
        return 2
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def norme(self):
        return sqrt(self.x**2+self.y**2)

    def normalize(self):
        a = self.norme()
        if not(a == 0):
            self.x /= a
            self.y /= a

    def __abs__(self):
        return self.norme()

    def __iter__(self):
        yield self.x
        yield self.y

    def __eq__(self,other):
        return self.x == other.x and self.y == other.y

    def __neq__(self,other):
        return not(self.__eq__(other))
    
    def to_array(self):
        return np.array([self.x,self.y])
    
    def from_list(list):
        return Vector2D(list[0],list[1])