"""
Universidad del Valle de Guatemala 
@author Marco Jurado 20308
"""
from collections import namedtuple
import struct
import glMatematica
from object import Obj
from object import Texture

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
    return bytes([b, g, r])

Black = color(0,0,0)
White = color(1,1,1)


# coordenadas baricentricas #
def coordenadasbaricentricas(A,B,C,k):
    lasbaricentricas = glMatematica.ProdCruz(
        V3(C.x - A.x, B.x - A.x, A.x - k.x), 
        V3(C.y - A.y, B.y - A.y, A.y - k.y)
    )

    if abs(lasbaricentricas[2]) < 1:
        return -1, -1, -1

    return (
        1 - (lasbaricentricas[0] + lasbaricentricas[1]) / lasbaricentricas[2], 
        lasbaricentricas[1] / lasbaricentricas[2], 
        lasbaricentricas[0] / lasbaricentricas[2]
    )

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

        self.zbuffer = [
            [-float('900') for x in range(self.width)] for y in range(self.height)
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
        try:
            self.pixels[ingy][ingx] = optColor or self.curr_color
        except:
        # To avoid index out of range exceptions
            pass

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

    def glTransform(self, vertex, translate=(0, 0, 0), scale=(1, 1, 1)):
    # returns a vertex 3, translated and transformed
        return V3(
        round((vertex[0] + translate[0]) * scale[0]),
        round((vertex[1] + translate[1]) * scale[1]),
        round((vertex[2] + translate[2]) * scale[2])
        )


    def glTriangle(self, A,B,C, clr=None,textureP=None,cordenadasTextura=(),intensidad=1):
        #evita llamar la funcion en el caso que la intensidad sea negativa (parte que no recibe nada de luz del modelo)
        if intensidad < 0:
            return

        minimo, maximo = glMatematica.Bounding(A, B, C)

        for x in range(minimo.x, maximo.x + 1):
            for y in range(minimo.y, maximo.y + 1):
                w, v, u = coordenadasbaricentricas(A, B, C, V2(x, y))
                if w < 0 or v < 0 or u < 0:  # 0 is actually a valid value! (it is on the edge)
                    continue
            
                # ahora se cargan las texturas con las coordenadas y la intensidad correspondiente
                if textureP:
                    # si tiene texturas
                    cordA, cordB, cordC = cordenadasTextura
                    tempX = cordA.x * w + cordB.x * v + cordC.x *u
                    tempY = cordA.y * w + cordB.y * v + cordC.y *u

                    

                    clr = textureP.get_color(tempX,tempY, intensidad) # se modifica el color a pintar para ser el correspondiente a la textura

                z = A.z * w + B.z * v + C.z * u

                if x > 0 and x < len(self.zbuffer) and y > 0 and y < len(self.zbuffer[0]):
                    if z > self.zbuffer[x][y]:
                        self.glVertex(x, y, clr)
                        self.zbuffer[x][y] = z

    
    """def glTriangleShading(self, A,B,C, cord=(), normal=(), clr=None):
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
                                self.glVertex(i,j,clr)"""



    def LoadModel(self,filename,translation=(0, 0, 0),scale=(1, 1, 1), textureP=None):
        # cargar modelo con texturas
        model = Obj(filename)
        luz = V3(0,0,1)
        for x in model.faces:
            #cada cara
            temp_vertices = len(x)
            if temp_vertices == 3:
                cara1 = x[0][0] - 1
                cara2 = x[1][0] - 1
                cara3 = x[2][0] - 1

                a = self.glTransform(model.vertices[cara1], translation, scale)
                b = self.glTransform(model.vertices[cara2], translation, scale)
                c = self.glTransform(model.vertices[cara3], translation, scale)
                
                norm = glMatematica.Normalizar( glMatematica.ProdCruz( glMatematica.Resta(b,a) , glMatematica.Resta(c,a) ) )
                intensidad = glMatematica.ProdPunto( norm, luz )
                grises = round(255 * intensidad)

                if not textureP:
                    # si el modelo no cuenta con texturas
                    if grises < 0:
                        continue

                    self.glTriangle(a, b, c, color( grises,grises,grises ))
                
                else: 
                    # si tiene texturas entonces buscamos A B C de las texturas para los triangulos
                    Textura_A = V2(*model.vtvertex[(x[0][1] - 1)])
                    Textura_B = V2(*model.vtvertex[(x[1][1] - 1)])
                    Textura_C = V2(*model.vtvertex[(x[2][1] - 1)])

                    print('hola', Textura_A,Textura_B,Textura_C)

                    #ahora se dibuja el triangulo
                    self.glTriangle(a,b,c,textureP=textureP, cordenadasTextura=(Textura_A, Textura_B, Textura_C), intensidad=intensidad)

            if temp_vertices == 4:
                cara1 = x[0][0] - 1
                cara2 = x[1][0] - 1
                cara3 = x[2][0] - 1
                cara4 = x[3][0] - 1

                a = self.glTransform(model.vertices[cara1], translation, scale)
                b = self.glTransform(model.vertices[cara2], translation, scale)
                c = self.glTransform(model.vertices[cara3], translation, scale)
                d = self.glTransform(model.vertices[cara4], translation, scale)

                
                norm = glMatematica.Normalizar( glMatematica.ProdCruz( glMatematica.Resta(a, b),  glMatematica.Resta(b, c) ) )
                intensidad = glMatematica.ProdPunto( norm, luz )
                grises = round(255 * intensidad)

                if not textureP:
                    # si el modelo no cuenta con texturas
                    if grises < 0:
                        continue

                    self.glTriangle(a, b, c, color( grises,grises,grises ))
                    self.glTriangle(a, c, d, color( grises,grises,grises ))
                
                else: 
                    # si tiene texturas entonces buscamos A B C de las texturas para los triangulos
                    Textura_A = V2(*model.vtvertex[(x[0][1] - 1)])
                    Textura_B = V2(*model.vtvertex[(x[1][1] - 1)])
                    Textura_C = V2(*model.vtvertex[(x[2][1] - 1)])
                    Textura_D = V2(*model.vtvertex[(x[3][1] - 1)])

                    #print('hola1', Textura_A,Textura_B,Textura_C, Textura_D)

                    #ahora se dibuja el triangulo
                    self.glTriangle(a,b,c,textureP=textureP, cordenadasTextura=(Textura_A, Textura_B, Textura_C), intensidad=intensidad)
                    self.glTriangle(a,c,d,textureP=textureP, cordenadasTextura=(Textura_A, Textura_C, Textura_D), intensidad=intensidad)


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

    def glFinishZBuffer(self,filename):
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
                temp = self.zbuffer[y][x]
                temp = int(temp)
                if temp < 0:
                    temp = 0
                if temp > 255:
                    temp = 255
                temp2 = color(temp,temp,temp)
                op.write(temp2)

        op.close()