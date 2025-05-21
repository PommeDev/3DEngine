import numpy as np
import Utils.Vector.Vector3D as V3
import numba as nb
#    I(theta) =  I(0)cos(theta)

@nb.njit
def diffuse_light_lambert(L,n):
    return max(np.dot(L,n),0)
