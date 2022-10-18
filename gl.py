"""
Universidad del Valle de Guatemala 
@author Marco Jurado 20308
"""
from collections import namedtuple
import struct
import glMatematica
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


# coordenadas baricentricas #
def coordenadasbaricentricas(A,B,C,k):
    areabc = (B.y - C.y) * (k.x - C.x) + (C.x - B.x) * (k.y - C.y)
    areaac = (C.y - A.y) * (k.x - C.x) + (A.x - C.x) * (k.y - C.y)
    areaabc = (B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y)

    try:
        #puntos u v w de las coordenadas baricentricas
        u = areabc / areaabc
        v = areaac / areaabc
        w = 1 - u - v
    except:
        return -1, -1, -1
    else:
        return u, v, w

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])


# render #

class Render(object):
    def __init__(self,width,height):
        self.colorBack = Black #color con el que se inicia el fondo en glClearColor

        self.width = width
        self.height = height

        self.viewX = 0
        self.viewY = 0

        self.curr_color = White
        self.curr_shade = None

        self.pixels = []

        self.glClearColor(0,0,0)
        self.glViewPort(0, 0, self.width, self.height)
        self.glClear()
        

    def glClear(self):
        self.pixels = [
            [self.colorBack for x in range (self.width)] for y in range (self.height)
        ]

        self.zBuffer = [
            [float('inf') for y in range(self.height)] for x in range(self.width)
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

    def glViewPort(self, x, y, w, h):
        #crea un viewport con los datos ingresados
        self.viewX = x
        self.viewY = y
        self.VPW = w
        self.VPH = h

        for x in range(self.viewX, self.viewX + self.VPW):
            for y in range(self.viewY, self.viewY + self.VPH):
                if (0 <= x < self.width) and (0 <= y < self.height):
                    self.pixels[x][y] = self.curr_color 

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

    def flatbottom(self,A,B,C,clr=None):
        " basado en explicación por Ing. Carlos "
        try:
            mBA = (B.x - A.x) / (B.y - A.y)
            mCA = (C.x - A.x) / (C.y - A.y)
        except:
            pass
        else:
            x0 = B.x
            x1 = C.x
            for y in range(int(B.y), int(A.y)):
                self.glLine(V2(x0, y), V2(x1, y), clr)
                x0 += mBA
                x1 += mCA

    def flatTop(self,A, B, C, clr=None):
        " basado en explicación por Ing. Carlos "
        try:
            mCA = (C.x - A.x) / (C.y - A.y)
            mCB = (C.x - B.x) / (C.y - B.y)
        except:
            pass
        else:
            x0 = A.x
            x1 = B.x
            for y in range(int(A.y), int(C.y), -1):
                self.glLine(V2(x0, y), V2(x1, y), clr)
                x0 -= mCA
                x1 -= mCB

    def glTriangle(self, A,B,C, clr=None):
        " basado en explicación por Ing. Carlos "
        if A.y < B.y:
            A, B = B, A
        if A.y < C.y:
            A, C = C, A
        if B.y < C.y:
            B, C = C, B

        self.glLine(A, B, clr)
        self.glLine(B, C, clr)
        self.glLine(C, A, clr)

        if B.y == C.y:
            #Cuando el triangulo tiene flat bottom
            self.flatBottom(A, B, C)
        elif A.y == B.y:
            #Cuando el triangulo tiene flat top
            self.flatTop(A, B, C)
        else:
            temp = V2(A.x + ((B.y - A.y) / (C.y - A.y)) * (C.x - A.x), B.y)
            self.flatBottom(A, B, temp)
            self.flatTop(B, temp, C)

    
    def glTriangleShading(self, A,B,C, cord=(), normal=(), clr=None):
        #se definen los minimos y maximos
        minimoX = round(min(A.x, B.x, C.x))
        minimoY = round(min(A.y, B.y, C.y))

        maximoX = round(max(A.x, B.x, C.x))
        maximoY = round(max(A.y, B.y, C.y))

        #la normal del triangulo normalizada
        TNormal =  glMatematica.Normalizar(glMatematica.ProdCruz( glMatematica.Resta( B,A ), glMatematica.Resta( C,A ) ))

        #con la normal del triangulo y generando las coordenadas baricentricas se puede generar el flat shade
        for i in range(minimoX, maximoY + 1):
            for j in range(minimoY, maximoX + 1):
                #dentro de los rangos de minimos y maximos
                u,v,w = coordenadasbaricentricas(A,B,C, V2(i,j)) #se generarn coordenadas 

                if u >= 0 and v >= 0 and w >= 0:
                    #si las coordenadas son mayor a 0
                    temp = A.temp * u + B.temp * v + C.temp * w 
                    if i >= 0 and i < self.width and j >= 0 and j < self.height:
                        if temp < self.zBuffer[i][j]:
                            self.zBuffer[i][j] = temp
                            if self.curr_shade:
                                r,g,b = self.curr_shade( self, coordenadasbaricentricas(u,v,w), optColor= clr or self.curr_color, cordenada = cord, N=normal, TNormal = TNormal)
                                self.glVertex(i,j,color(r,g,b))
                            else: 
                                self.glVertex(i,j,clr)



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