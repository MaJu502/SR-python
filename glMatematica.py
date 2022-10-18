"""
@author Marco Jurado
Para no hacer uso de librerias externas se crea dicho 
archivo con la finalidad de realizar la matematica 
necesaria para operar vectores y demás.areaac
"""
import math 

def ProdCruz(a,b):
    return [ 
        (a[1]*b[2] - a[2]*b[1]),
        (a[2]*b[0] - a[0]*b[2]),
        (a[0]*b[1] - a[1]*b[0])
    ]

def Resta(a,b):
    retorno = []
    for i in range (len(a)):
        #por cada elemento de a
        retorno.append(a[i] - b[i]) #se resta cada elemento de b en la misma posicion

    return retorno

def Normalizar(x):
    temp = math.sqrt( x[0]**2 + x[1]**2 + x[2]**2 )
    return [ 
        x[0]/temp, x[1]/temp, x[2]/temp
     ]

