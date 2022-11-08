from gl import *
from object import Texture
from math import pi

def menu():
    r = Render(800, 800)
    texture_pack = 'marte'
    r.light = V3(0,0,1)
    r.glClearColor(0, 0, 0)
    r.glClear()
    translation = (0,0,0)
    scale = (0.5,0.5,0.5)
    rotation = ( 0.1, 0, 0 )

    r.lookAT(V3(0,-20,65), V3(0,0,0), V3(30,50,0))
    r.LoadModel('./Stylized_Planets.obj', translation, scale, rotation, texture_pack)
    r.glFinish("ShaderOUT.bmp")
    r.glFinishZBuffer("ShaderOUT_ZBuffer.bmp")

menu()