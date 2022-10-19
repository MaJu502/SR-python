from gl import *
from object import Texture

r = Render(600, 600)
texture_pack = Texture('./plant.bmp')
r.glClearColor(0, 0, 0)
r.glClear()
r.LoadModel('./plant.obj', (5,4,1), (50,50,50), textureP=texture_pack)
r.glFinish("out.bmp")
r.glFinishZBuffer("outZBUFFED.bmp")