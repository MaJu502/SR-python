from gl import *
from object import Texture

r = Render(600, 600)
texture_pack = Texture('./plant.bmp')
r.glClearColor(0, 0, 0)
r.glClear()
r.LoadModel('./plant.obj', (5,4,1), (50,50,50), textureP=texture_pack)
r.glFinish("out.bmp")
r.glFinishZBuffer("outZBUFFED.bmp")

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

        if opcion == 1:
            continue
        elif opcion == 2:
            continue
        elif opcion == 3:
            continue
        elif opcion == 4:
            continue
        elif opcion == 5:
            salir = True
        else: 
            print("opcion invalida porfavor intenta nuevamente")
