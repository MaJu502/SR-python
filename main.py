from gl import *

r = Render(600, 600)
r.glClearColor(0, 0, 0)
r.glClear()
r.LoadModel('./plant.obj', (0.5,0.5,0.5), (0.5,0.5,0.5))
r.glFinish("out.bmp")