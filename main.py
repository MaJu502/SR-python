from gl import *
from object import Texture

r = Render(600, 600)
texture_pack = Texture('./plant.bmp')
r.light = V3(0,0,1)
r.glClearColor(0, 0, 0)
r.glClear()

r.lookAT(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))


r.load('./models/model.obj', translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0))
r.LoadModel('./plant.obj', (5,4,1), (50,50,50), (0,0,0), textureP=texture_pack)
r.glFinish("out111.bmp")
r.glFinishZBuffer("outZBUFFED111.bmp")

"""
def menu():
    salir = False
    while salir == False:

        print("bienvenido! selecciona el angulo de camara que deseas generar:")
        print("   1.  Medium Shot ")
        print("   2.  Low Angle ")
        print("   3.  High Angle ")
        print("   4.  Dutch Angle ")
        print("   5.  SALIR DE PROGRAMA ")

        opcion = input()

        transform = (0,0,0)
        scale = (0,0,0)
        rotation = (0,0,0)

        if opcion == 1:
            r.LoadModel('./plant.obj', (5,4,1), (50,50,50), textureP=texture_pack)
            r.glFinish("out.bmp")
            r.glFinishZBuffer("outZBUFFED.bmp")
        elif opcion == 2:
            r.LoadModel('./plant.obj', (5,4,1), (50,50,50), textureP=texture_pack)
            r.glFinish("out.bmp")
            r.glFinishZBuffer("outZBUFFED.bmp")
        elif opcion == 3:
            r.LoadModel('./plant.obj', (5,4,1), (50,50,50), textureP=texture_pack)
            r.glFinish("out.bmp")
            r.glFinishZBuffer("outZBUFFED.bmp")
        elif opcion == 4:
            r.LoadModel('./plant.obj', (5,4,1), (50,50,50), textureP=texture_pack)
            r.glFinish("out.bmp")
            r.glFinishZBuffer("outZBUFFED.bmp")
        elif opcion == 5:
            salir = True
        else: 
            print("opcion invalida porfavor intenta nuevamente")
"""