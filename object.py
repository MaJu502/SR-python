#cargar archivos obj
from re import X


class Obj(object):
    def __init__(self, filename):
        self.vertices = []
        self.faces = []
        with open(filename) as f:
            self.lines = f.read().splitlines()


        for line in self.lines:
            #por cada linea del archivo obj
            try:
                prefix, value = line.split(' ', 1) #split para obtener el tipo de dato que es cara o vertice
            except:
                continue

            match prefix:
                case 'v':
                    #vertice
                    vertex = [float(x) for x in value.split(' ')]
                    self.vertices.append(vertex) #guarda el vertice

                case'f' :
                    #cara
                    caritas = [[int(x) for x in f.split('/')] for f in value.split(' ')]
                    self.faces.append(caritas) #guarda el vertice #guarda la cara