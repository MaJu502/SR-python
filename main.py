from gl import *

r = Render(500, 500)
r.glClearColor(0, 0, 0)
r.glClear()
r.LoadModel('./fish.obj', ((500/2.5), (500/2)), (60,60), (2,1))
r.glFinish("fish.bmp")