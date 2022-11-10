from gl import *
from object import Texture
from math import pi

r = Render(800, 800)
# --------------------------------------- chest --------------------------------------
print('starting chest')
texture_pack = Texture('./models/chest.bmp')
r.light = V3(0,0,1)
r.glClearColor(0, 0, 0)
r.glClear()
r.background('./models/background.bmp')
translation = (0.6,-0.6,0)
scale = (0.6,0.6,0.6)
rotation = ( 2.5, 1, 3.1)

r.lookAT(V3(0,5,5), V3(0,0,0), V3(0,1,0))
r.LoadModel('./models/chest.obj', translation, scale, rotation, textureP=texture_pack)
print('done chest')

# --------------------------------------- plant --------------------------------------
print('starting plant')
texture_pack = Texture('./models/plant.bmp')
r.light = V3(0,0,1)
translation = (0.6,0.25,0.2)
scale = (0.05,0.05,0.05)
rotation = ( -0.8, 0, 0 )

r.lookAT(V3(0,5,5), V3(0,0,0), V3(0,1,0))
r.LoadModel('./models/plant.obj', translation, scale, rotation, textureP=texture_pack)
print('done plant')

# --------------------------------------- shoe --------------------------------------
print('starting shoe')
texture_pack = Texture('./models/shoe.bmp')
r.light = V3(0,0,1)
translation = (-0.6,-0.4,0.2)
scale = (0.03,0.03,0.03)
rotation = ( -1.5, 0, 1 )

r.lookAT(V3(0,0,5), V3(0,0,0), V3(0,1,0))
r.LoadModel('./models/shoe.obj', translation, scale, rotation, textureP=texture_pack)
print('done shoe')

# --------------------------------------- poundcake --------------------------------------
print('starting poundcake')
texture_pack = Texture('./models/poundcake.bmp')
r.light = V3(0,0,1)
translation = (-0.2,-0.4,2)
scale = (0.02,0.02,0.02)
rotation = ( 2.5, 1.5, 0.7 )

r.lookAT(V3(0,0,5), V3(0,0,0), V3(0,1,0))
r.LoadModel('./models/poundcake.obj', translation, scale, rotation, textureP=texture_pack)
print('done poundcake')

# --------------------------------------- Shiba --------------------------------------
print('starting Shiba')
texture_pack = 'shiba'
r.light = V3(0,0,1)
translation = (0.2,-0.7,0)
scale = (3,3,3)
rotation = ( 0,-0.8,0 )

r.lookAT(V3(0,0,5), V3(0,0,0), V3(0,1,0))
r.LoadModel('./models/Shiba.obj', translation, scale, rotation, textureP=texture_pack)
print('done Shiba')

r.glFinish("Scene.bmp")
r.glFinishZBuffer('ZBuffed_Scene.bmp')