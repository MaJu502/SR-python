from gl import *

r = Render(600, 600)
r.glClearColor(0, 0, 0)
r.glClear()
r.LoadModel('./plant.obj', (5,4,1), (50,50,50))
r.glFinish("out.bmp")
r.glFinishZBuffer("outZBUFFED.bmp")