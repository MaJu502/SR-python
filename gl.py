"""
Universidad del Valle de Guatemala 
@author Marco Jurado 20308
"""
from collections import namedtuple
from re import X
import struct
import glMatematica
from object import Obj
from object import Texture
from math import cos,sin
from shader import *

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

        self.light = V3(0,0,1)
        self.vArray = []

        self.pixels = []

        self.View = None
        self.Model = None

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


    """def rounding(self, x):
        retorno = V3(0,0,0)

        print('hey < ', x[0])

        for i in x:
            if i < 0:
                i = 0
                print(i)
            else:
                i = round(i)
                print(i)
        print('la xxxxxttttreme > ', x )
        return x"""
        

    def glTriangle(self, A,B,C, clr=None,textureP=None,cordenadasTextura=(),intensidad=1,**kwargs):
        
        minimo, maximo = glMatematica.Bounding(A, B, C)
        grises = round(255 * intensidad)
        #se debe de definir una nueva intensidad con el movimiento de las camaras
        intensidad = glMatematica.ProdPunto(glMatematica.Normalizar( glMatematica.ProdCruz(glMatematica.Resta(B,A), glMatematica.Resta(C,A))), self.light)

        #evita llamar la funcion en el caso que la intensidad sea negativa (parte que no recibe nada de luz del modelo)
        if intensidad < 0:
            return
        
        for x in range(round(minimo.x), round(maximo.x) + 1):
            for y in range(round(minimo.y), round(maximo.y) + 1):
                w, v, u = coordenadasbaricentricas(A, B, C, V2(x, y))
                if w < 0 or v < 0 or u < 0:  # 0 is actually a valid value! (it is on the edge)
                    continue
            
                # ahora se cargan las texturas con las coordenadas y la intensidad correspondiente
                if textureP == 'shiba':
                    cordA, cordB, cordC = cordenadasTextura
                    tempX = cordA.x * w + cordB.x * v + cordC.x *u
                    tempY = cordA.y * w + cordB.y * v + cordC.y *u

                    #hace Shiba
                    colorNep = Shiba(y = y,x = x , cord_baricentricas = (w,u,v), luz= V3(0,0,1), normales=kwargs['normales'])
                    if colorNep == (0,0,0):
                        r,g,b = grises, grises, grises

                    else:
                        r,g,b = colorNep
                        b = round(b * 255 * intensidad)
                        g = round(g * 255 * intensidad)
                        r = round(r * 255 * intensidad)

                    z = A.z * w + B.z * v + C.z * u

                    if x > 0 and x < len(self.zbuffer) and y > 0 and y < len(self.zbuffer[0]):
                        if z > self.zbuffer[x][y]:
                            self.glVertex(x, y, color(r,g,b))
                            self.zbuffer[x][y] = z

                if textureP != 'shiba':
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



    def LoadModel(self,filename,translation=(0, 0, 0),scale=(1, 1, 1), rotation=(0,0,0), textureP=None):
        # cargar modelo con texturas
        self.loadModelMatrix(translation,scale,rotation)
        model = Obj(filename)
        luz = V3(0,0,1)
        for x in model.faces:
            #cada cara
            temp_vertices = len(x)
            if temp_vertices == 3:
                cara1 = x[0][0] - 1
                cara2 = x[1][0] - 1
                cara3 = x[2][0] - 1

                a = self.transformar(model.vertices[cara1])
                b = self.transformar(model.vertices[cara2])
                c = self.transformar(model.vertices[cara3])
                
                norm = glMatematica.Normalizar( glMatematica.ProdCruz( glMatematica.Resta(b,a) , glMatematica.Resta(c,a) ) )
                intensidad = glMatematica.ProdPunto( norm, luz )
                grises = round(255 * intensidad)

                if not textureP:
                    # si el modelo no cuenta con texturas
                    if grises < 0:
                        continue

                    self.glTriangle(a, b, c, color( grises,grises,grises ))
                
                if textureP == 'shiba':
                    Textura_A = V2(*model.vtvertex[(x[0][1] - 1)])
                    Textura_B = V2(*model.vtvertex[(x[1][1] - 1)])
                    Textura_C = V2(*model.vtvertex[(x[2][1] - 1)])
                    self.glTriangle(a,b,c,textureP='shiba', cordenadasTextura=(Textura_A, Textura_B, Textura_C), intensidad=intensidad , normales=norm)
                
                
                else: 
                    # si tiene texturas entonces buscamos A B C de las texturas para los triangulos
                    Textura_A = V2(*model.vtvertex[(x[0][1] - 1)])
                    Textura_B = V2(*model.vtvertex[(x[1][1] - 1)])
                    Textura_C = V2(*model.vtvertex[(x[2][1] - 1)])

                    #ahora se dibuja el triangulo
                    self.glTriangle(a,b,c,textureP=textureP, cordenadasTextura=(Textura_A, Textura_B, Textura_C), intensidad=intensidad)

            if temp_vertices == 4:
                cara1 = x[0][0] - 1
                cara2 = x[1][0] - 1
                cara3 = x[2][0] - 1
                cara4 = x[3][0] - 1


                a = self.transformar(model.vertices[cara1])
                b = self.transformar(model.vertices[cara2])
                c = self.transformar(model.vertices[cara3])
                d = self.transformar(model.vertices[cara4])

                
                norm = glMatematica.Normalizar( glMatematica.ProdCruz( glMatematica.Resta(a, b),  glMatematica.Resta(b, c) ) )
                intensidad = glMatematica.ProdPunto( norm, luz )
                grises = round(255 * intensidad)

                if not textureP:
                    # si el modelo no cuenta con texturas
                    if grises < 0:
                        continue

                    self.glTriangle(a, b, c, color( grises,grises,grises ))
                    self.glTriangle(a, c, d, color( grises,grises,grises ))

                if textureP == 'shiba':
                    Textura_A = V2(*model.vtvertex[(x[0][1] - 1)])
                    Textura_B = V2(*model.vtvertex[(x[1][1] - 1)])
                    Textura_C = V2(*model.vtvertex[(x[2][1] - 1)])
                    Textura_D = V2(*model.vtvertex[(x[3][1] - 1)])

                    self.glTriangle(a,b,c,textureP='shiba', cordenadasTextura=(Textura_A, Textura_B, Textura_C), intensidad=intensidad , normales=norm)
                    self.glTriangle(a,c,d,textureP='shiba', cordenadasTextura=(Textura_A, Textura_B, Textura_C), intensidad=intensidad , normales=norm)
                
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
    
    def lookAT(self, eye, center, up):
        z = ( glMatematica.Normalizar( glMatematica.Resta(eye,center) ) )
        x = ( glMatematica.Normalizar( glMatematica.ProdCruz(up, z) ) )
        y = ( glMatematica.Normalizar( glMatematica.ProdCruz(z,x) ) )
        self.loadViewMatrix(x, y, z, center)
        self.loadProjectionMatrix(-1/glMatematica.largoVector( glMatematica.Resta(eye,center) ))
        self.loadViewportMatrix()

    def loadViewMatrix(self, x, y, z, center):
        Matriz1 = ([[x.x, x.y, x.z,  0], [y.x, y.y, y.z, 0], [z.x, z.y, z.z, 0], [0, 0, 0, 1]])
        Matriz2 = ([[1, 0, 0, -center.x], [0, 1, 0, -center.y], [0, 0, 1, -center.z], [0, 0, 0, 1]])
        self.View = glMatematica.multiplicarMatriz44(Matriz1, Matriz2)

    def loadProjectionMatrix(self, coeff):
        self.Projection = ([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, coeff, 1]])

    def loadViewportMatrix(self, x = 0, y = 0):
        self.Viewport = ([[self.width/2, 0, 0, x + self.width/2], [0, self.height/2, 0, y + self.height/2], [0, 0, 128, 128], [0, 0, 0, 1]])

    def loadModelMatrix(self, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
        translate = V3(*translate)
        scale = V3(*scale)
        rotate = V3(*rotate)
        
        translation_matrix = [[1, 0, 0, translate.x], [0, 1, 0, translate.y], [0, 0, 1, translate.z], [0, 0, 0,1]]
        scale_matrix = [[scale.x, 0, 0, 0], [0, scale.y, 0, 0], [0, 0, scale.z, 0], [0, 0, 0, 1]]
    
        rotar_matrizX = [[1, 0, 0, 0], [0, cos(rotate.x), -sin(rotate.x), 0], [0, sin(rotate.x),  cos(rotate.x), 0],[0, 0, 0, 1]]
        rotar_matrizY = [[cos(rotate.y), 0, sin(rotate.y), 0],[0, 1, 0, 0], [-sin(rotate.y), 0, cos(rotate.y), 0], [0, 0, 0, 1]]
        rotar_matrizZ = [[cos(rotate.z), -sin(rotate.z), 0, 0], [sin(rotate.z),  cos(rotate.z), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

        "con las matrices de x,y,z se puede obtener la matriz de rotacion al multiplicarlas"
        rotation_matrix = glMatematica.multiplicarMatriz44(rotar_matrizX, glMatematica.multiplicarMatriz44(rotar_matrizY, rotar_matrizZ))

        self.Model = glMatematica.multiplicarMatriz44(translation_matrix, glMatematica.multiplicarMatriz44(rotation_matrix, scale_matrix))

    def transformar(self, v):
        tempVertices = [v[0] , v[1], v[2], 1]

        "sustituyendo el uso de numpy para multiplicar estas matrices se reailza lo siguiente"

        temp1 = glMatematica.multiplicarMatriz44(self.Viewport, self.Projection)
        temp2 = glMatematica.multiplicarMatriz44(temp1, self.View)
        temp3 = glMatematica.multiplicarMatriz44(temp2, self.Model)
        temp4 = glMatematica.multiplicarMatriz44(temp3, [ [x] for x in tempVertices ])
        temp4 = [[i[0] for i in temp4]]

        tranformed_vertex = temp4[0]

        tranformed_vertex = [
        (tranformed_vertex[0]/tranformed_vertex[3]), 
        (tranformed_vertex[1]/tranformed_vertex[3]), 
        (tranformed_vertex[2]/tranformed_vertex[3])
        ]

        return V3(*tranformed_vertex)

    def background(self,file):
        img = Texture(file)
        self.pixels = img.pixels

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

        print(' DIOOOOOOOOOOS ESTAAAAAAA AQUIIIIIIII...')
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