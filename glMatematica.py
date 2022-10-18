"""
@author Marco Jurado
Para no hacer uso de librerias externas se crea dicho 
archivo con la finalidad de realizar la matematica 
necesaria para operar vectores y demás.areaac
"""
import math 
from collections import namedtuple
V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])

def ProdCruz(a,b):
    return V3(
        a.y * b.z - a.z * b.y,
        a.z * b.x - a.x * b.z,
        a.x * b.y - a.y * b.x,
    )

def Resta(a,b):
    return V3(a.x - b.x, a.y - b.y, a.z - b.z)

def Normalizar(a):
    temp = (a.x**2 + a.y**2 + a.z**2)**0.5
    if not temp:
        return V3(0,0,0)

    return V3(a.x/temp, a.y/temp, a.z/temp)

def ProdPunto(a,b):
    return a.x * b.x + a.y * b.y + a.z * b.z


def Bounding(*vertices):
    xs = [ vertex.x for vertex in vertices ]
    ys = [ vertex.y for vertex in vertices ]
    xs.sort()
    ys.sort()

    return V2(xs[0], ys[0]), V2(xs[-1], ys[-1])