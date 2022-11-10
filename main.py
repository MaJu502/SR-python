from gl import *
from object import Texture
from math import pi

r = Render(800, 800)
# --------------------------------------- log --------------------------------------
texture_pack = Texture('./models/woodenlog.bmp')
r.light = V3(0,0,1)
r.glClearColor(0, 0, 0)
r.glClear()
translation = (-0.6,-0.6,0)
scale = (0.6,0.6,0.6)
rotation = ( 0.1, 0, 0 )

r.lookAT(V3(0,5,5), V3(0,0,0), V3(0,1,0))
r.LoadModel('./models/woodenlog.obj', translation, scale, rotation, textureP=texture_pack)
print('done log')

# --------------------------------------- plant --------------------------------------
texture_pack = Texture('./models/plant.bmp')
r.light = V3(0,0,1)
translation = (-0.6,0.1,0.2)
scale = (0.1,0.1,0.1)
rotation = ( 0.1, 0, 0 )

r.lookAT(V3(0,5,5), V3(0,0,0), V3(0,1,0))
r.LoadModel('./models/plant.obj', translation, scale, rotation, textureP=texture_pack)
print('done plant')

# --------------------------------------- shoe --------------------------------------
texture_pack = Texture('./models/shoe.bmp')
r.light = V3(0,0,1)
translation = (0,-0.5,0.2)
scale = (0.05,0.05,0.05)
rotation = ( -1.5, 0, 1 )

r.lookAT(V3(0,5,5), V3(0,0,0), V3(0,1,0))
r.LoadModel('./models/shoe.obj', translation, scale, rotation, textureP=texture_pack)
print('done shoe')






r.glFinish("Scene.bmp")
"""r.glFinishZBuffer("Scenezbuf.bmp")"""

"""
def menu():
    r = Render(800, 800)
    texture_pack = Texture('./plant.bmp')
    r.light = V3(0,0,1)
    r.glClearColor(0, 0, 0)
    r.glClear()

    print('Bienvenido! selecciona una opción para comenzar')
    salir = False
    while salir == False:
        print(' 1. Medium Shot ')
        print(' 2. Low Angle ')
        print(' 3. High Angle ')
        print(' 4. Dutch Angle ')
        print(' 5. Salir ')

        opcion = input()

        if opcion == '1':
            #medium shot
            translation = (0,-1.2,0)
            scale = (0.15,0.15,0.15)
            rotation = ( 0.1, 0, 0 )

            r.lookAT(V3(0,0,5), V3(0,0,0), V3(0,1,0))
            r.LoadModel('./plant.obj', translation, scale, rotation, textureP=texture_pack)
            r.glFinish("MediumShot.bmp")
            r.glFinishZBuffer("MediumShot_ZBuffer.bmp")

        elif opcion == '2':
            #low angle
            translation = (0,-0.6,0)
            scale = (0.16,0.16,0.16)
            rotation = ( 0.1, 0, 0 )

            r.lookAT(V3(0,-10,10), V3(0,0,0), V3(0,1,0))
            r.LoadModel('./plant.obj', translation, scale, rotation, textureP=texture_pack)
            r.glFinish("LowAngle.bmp")
            r.glFinishZBuffer("LowAngle_ZBuffer.bmp")
        elif opcion == '3':
            #high angle
            translation = (0,-0.6,0)
            scale = (0.16,0.16,0.16)
            rotation = ( 0.1, 0, 0 )

            r.lookAT(V3(0,65,65), V3(0,0,0), V3(0,1,0))
            r.LoadModel('./plant.obj', translation, scale, rotation, textureP=texture_pack)
            r.glFinish("HighAngle.bmp")
            r.glFinishZBuffer("HighAngle_ZBuffer.bmp")
        
        elif opcion == '4':
            #dutch angle
            translation = (0,-0.6,0)
            scale = (0.16,0.16,0.16)
            rotation = ( 0.1, 0, 0 )

            r.lookAT(V3(0,-20,65), V3(0,0,0), V3(30,50,0))
            r.LoadModel('./plant.obj', translation, scale, rotation, textureP=texture_pack)
            r.glFinish("DutchAngle.bmp")
            r.glFinishZBuffer("DutchAngle_ZBuffer.bmp")
            
        elif opcion == '5':
            #salir
            print('Gracias por utilizar el programa. Hasta pronto!')
            salir = True
        else:
            print('ingresa una opcion valida')

menu()"""