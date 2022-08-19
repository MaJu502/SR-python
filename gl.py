"""
Universidad del Valle de Guatemala 
Autor: Marco Jurado 20308
Creation Date: 7/7/22
Last Update: 18/8/22
"""
import struct

from object import Obj

# char, word, double word #
def ch(x):
    return struct.pack('=c',x.encode('ascii'))
def wrd(x):
    return struct.pack('=h', x)
def dwrd(x):
    return struct.pack('=l', x)

# colors #
def color(r,g,b):
    # number between 0 and 255 for each input
    return bytes([int(b * 255), int(g * 255), int(r * 255)])
Black = color(0,0,0)
White = color(1,1,1)

# render #

class Render(object):
    def __init__(self,width,height):
        self.colorBack = Black #color con el que se inicia el fondo en glClearColor
        self.width = width
        self.height = height
        self.viewX = 0
        self.viewY = 0
        self.curr_color = White
        self.pixels = []
        self.glClearColor(0,0,0)
        self.glViewPort(0, 0, self.width, self.height)
        

    def glClear(self):
        self.pixels = [
            [self.colorBack for x in range (self.width)] for y in range (self.height)
        ]
    
    def glClearColor(self, r, g, b):
        self.colorBack = color(r, b, g)
        self.glClear()

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()

    #def glClearViewport(self, ):
    
    def glColor(self, r, g, b):
        #color con el que funciona vertex
        self.curr_color = color(r,g,b)

    def glViewPort(self, x, y, w, h, colo=White):
        #crea un viewport con los datos ingresados
        self.viewX = x
        self.viewY = y
        self.VPW = w
        self.VPH = h

        for x in range(self.viewX, self.viewX + self.VPW):
            for y in range(self.viewY, self.viewY + self.VPH):
                if (0 <= x < self.width) and (0 <= y < self.height):
                    self.pixels[x][y] = colo or self.curr_color 

    def glVertex(self, ingx, ingy, optColor=None):
        if ingx > 1 or ingx < -1 or ingy > 1 or ingy < -1:
            self.pixels[ingx][ingy] = self.curr_color
        else:
            x = int((ingx + 1) * (self.VPW / 2) + self.viewX)
            y = int((ingy + 1) * (self.VPH / 2) + self.viewY)
            self.pixels[x][y] = optColor or self.curr_color

    def glLine(self,x0,y0,x1,y1, optColor=None):
        x0,y0 = y0,x0
        x1,y1=y1,x1

        cambioy = abs(y1-y0)
        cambiox = abs(x1-x0)
        pendiente = cambioy > cambiox


        if pendiente:
            #si el cambio en y es mayo a el cambio en x
            #se invierten los puntos para dibujar la linea
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            #en el caso que el primer punto tenga la coordenada
            #x arriba del segundo punto
            x0,x1 = x1, x0
            y0, y1 = y1, y0
        
        cambioy = abs(y1-y0)
        cambiox = abs(x1-x0)

        off = 0
        thresh = cambiox

        inicio = y0

        for punto in range(x0,x1+1):
            #por cada punto desde el primer x sumandole 1 hasta llegar al ultimo x de la linea
            if pendiente:
                self.glVertex(inicio, punto, optColor)
            else:
                self.glVertex(punto,inicio,optColor)

            off += cambioy * 2
            if off >= thresh:
                #si el offset de la linea es mayor al threshold
                inicio += 1 if y0 < y1 else -1
                thresh += cambiox * 2

    def glDrawFig(self, ElementosFig:list[list]):
        """ recibe una lista de listas que contiene cada pixel del archivo
            para dibujar la totalidad de la figura"""

        for linea in range(0,len(ElementosFig)):
            #se tienen que definir los puntos iniciales de la tupla de coordenadas
            ix = ElementosFig[linea][0] #coord en x
            iy = ElementosFig[linea][1] #coord en y
            xf,yf = 0,0

            temp = linea < len(ElementosFig) - 1
            match temp:
                case True:
                    #por cada tupla de coordenadas en la lista de la figura
                    xf = ElementosFig[linea+1][0] #coord en x
                    yf = ElementosFig[linea+1][1] #coord en y

                case False:
                    """en el caso que se llegue a la ultima coordenada de la figura se debe de trazar la linea
                    hacia la primer coordenada para cerrar la figura"""
                    xf = ElementosFig[0][0]
                    yf = ElementosFig[0][1]

            self.glLine(ix, iy, xf, yf)

    def EvenOdd(self, x, y, polygon):
        #basado en algoritmo de Even-Odd Rule
        """ x, y son las coordenadas del punto 
            para comenzar a rellenar la figura """

        Tamano_poly = len(polygon)
        temp = Tamano_poly -1
        Esta_dentro = False

        for i in range(Tamano_poly):
            if (x == polygon[i][0]) and (y == polygon[i][1]):
                #esquina
                return True
            if ((polygon[i][1] > y) != (polygon[temp][1] > y)):
                pendiente = (x-polygon[i][0])*(polygon[temp][1]-polygon[i][1]) - (polygon[temp][0]-polygon[i][0])*(y-polygon[i][1])
                if pendiente == 0:
                    #perimetro
                    return True

                if (pendiente < 0) != (polygon[temp][1] < polygon[i][1]):
                    Esta_dentro = not Esta_dentro
            temp = i
        return Esta_dentro

    def glFillPolygon(self, polygon, optColor):
        for x in range(self.width):
            #recorre la pantalla en el eje x
            for y in range(self.height):
                #recorre la pantalla en el eje y
                if self.EvenOdd(y,x,polygon):
                    self.glVertex(x,y,optColor)


    def LoadModel(self,filename,translation,scale,cord):
        objs = Obj(filename)
        for x in objs.faces:
            #cada cara
            temp_vertices_cara = [] #los vertices que conforman la cara
            for y in x:
                #cada coordenada dentro de la cara seleccionada
                temp_vertice_dibujar = [
                    int(round((objs.vertices[y[0] - 1])[cord[0]] * scale[0]) + translation[0]),
                    int(round((objs.vertices[y[0] - 1])[cord[1]] * scale[1]) + translation[1])
                ]
                for temp in temp_vertice_dibujar:
                    temp = int(temp)
                temp_vertices_cara.append(temp_vertice_dibujar)
            self.glDrawFig(temp_vertices_cara)
                


    def glFinish(self,filename):
        op = open(filename, 'bw')

        #Header
        op.write(ch('B'))
        op.write(ch('M'))
        op.write(dwrd( 14 + 40 + (self.width * self.height * 3)))
        op.write(dwrd(0))
        op.write(dwrd(14 + 40))

        #Image
        op.write(dwrd(40))
        op.write(dwrd(self.width))
        op.write(dwrd(self.height))
        op.write(wrd(1))
        op.write(wrd(24))
        op.write(dwrd(0))
        op.write(dwrd(self.width * self.height * 3)) #screen size
        op.write(dwrd(0))
        op.write(dwrd(0))
        op.write(dwrd(0))
        op.write(dwrd(0))

        #Color/Pixel data
        for x in range(self.height):
            for y in range(self.width):
                op.write(self.pixels[x][y])

        op.close()