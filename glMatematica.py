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

def Suma(a,b):
    return V3(a.x + b.x, a.y + b.y, a.z + b.z)

def Multiplicacion(a,k):
    return V3(a.x * k, a.y * k, a.z * k)

def largoVector(a):
    return (a.x**2 + a.y**2 + a.z**2)**0.5

def multiplicarMatriz44(a,b):
    """adaptado con referencia a la página web donde se define un ejemplo de multiplicacion de matriz sin numpy
    https://www.knowprogram.com/python/python-matrix-multiplication-without-numpy/
    """

    retorno = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]

    for i in range(len(a)):
        "cada fila de la matriz a"
        for x in range(len(b)):
            "cada fila de la matriz b"
            for y in range(len(b)):
                """por cada fila de la matriz a se toma la fila de la matriz b y se realiza
                a continuación cada fila de la matriz b con todas las filas de la matriz b"""
                if isinstance(b[0], int) or isinstance(b[0], float):
                    "se añade el caso que en la matriz b tengamos un entero o un float"
                    retorno[i][x] += a[i][y] * b[y]
                elif isinstance(a[0], int) or isinstance(a[0], float):
                    "se añade el caso que en la matriz a tengamos un entero o un float"
                    retorno[i][x] += a[y] * b[y][x]
                else:
                    "caso base"
                    retorno[i][x] += a[i][y] * b[y][x]