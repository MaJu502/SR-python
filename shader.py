"""
Universidad del Valle de Guatemala 
@author Marco Jurado 20308
"""
import glMatematica

def neptuno(r,**kwargs):
    #con el uso del algoritmo de gourad se crea una textura similar a la del planeta neptuno
    x,y = kwargs['cordenadas']
    width,height = kwargs['tamaño']
    #primero obtenemos la intensidad de la luz
    w,u,v = kwargs['cord_baricentricas']
    normA, normB, normC = kwargs['normales']

    intensidadA = glMatematica.ProdPunto(glMatematica.Normalizar(normA), glMatematica.Normalizar(kwargs['luz']))
    intensidadB = glMatematica.ProdPunto(glMatematica.Normalizar(normB), glMatematica.Normalizar(kwargs['luz']))
    intensidadC = glMatematica.ProdPunto(glMatematica.Normalizar(normC), glMatematica.Normalizar(kwargs['luz']))

    temp_intensidad = intensidadA * w + intensidadB * u + intensidadC * v

