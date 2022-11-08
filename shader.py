"""
Universidad del Valle de Guatemala 
@author Marco Jurado 20308
"""
import glMatematica

def marte(**kwargs):
    #con el uso del algoritmo de gourad se crea una textura similar a la del planeta marte
    """x = kwargs['x']
    y = kwargs['y']
    width = kwargs['width']
    height = kwargs['height']"""
    y = kwargs['y']
    x = kwargs['x']
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
    
    cafe = (190/255,160/255,119/255)
    cafe_oscuro = (162/255,126/255,93/255)
    cafe_mediocafe = (184/255,172/255,150/255)

    cafe_luna = (201/255,178/255,146/255)


    if y < 200:
        color = cafe
    if y > 199:
        color = cafe_oscuro
    if y > 300:
        color = cafe_mediocafe
    if y > 400:
        color = cafe

    if x > 600:
        color = cafe_luna
    return color


        

