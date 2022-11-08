"""
Universidad del Valle de Guatemala 
@author Marco Jurado 20308
"""
import glMatematica

def neptuno(**kwargs):
    #con el uso del algoritmo de gourad se crea una textura similar a la del planeta neptuno
    """x = kwargs['x']
    y = kwargs['y']
    width = kwargs['width']
    height = kwargs['height']"""
    y = kwargs['y']
    #primero obtenemos la intensidad de la luz
    w,u,v = kwargs['cord_baricentricas']
    normA, normB, normC = kwargs['normales']

    """print('lux  > ', kwargs['luz'])
    print('normA  >  ', normA)
    print('normB  >  ', normB)
    print('normC  >  ', normC)

    intensidadA = glMatematica.ProdPunto(glMatematica.Normalizar(normA), glMatematica.Normalizar(kwargs['luz']))
    intensidadB = glMatematica.ProdPunto(glMatematica.Normalizar(normB), glMatematica.Normalizar(kwargs['luz']))
    intensidadC = glMatematica.ProdPunto(glMatematica.Normalizar(normC), glMatematica.Normalizar(kwargs['luz']))

    temp_intensidad = intensidadA * w + intensidadB * u + intensidadC * v"""

    color = (0,0,0)
    
    azul = (0,0,1)

    if y > 500:
        color = azul
    return color


        

