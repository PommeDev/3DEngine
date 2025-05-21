from Utils.Vector import Vector3D,Vector2D

class Vertex:
    def __init__(self,pos:Vector3D.Vector3D = Vector3D.Vector3D(), uv:Vector2D.Vector2D = Vector2D.Vector2D()):
        self.pos = pos
        self.uv = uv

    