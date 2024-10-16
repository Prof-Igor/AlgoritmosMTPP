class Vertice:
    def __init__(self, nome, idCor):
        self.nome = nome
        self.idCor = idCor
        self.idCores = []


class Grafo:
    def __init__(self, nVertices, nCores, nArestas):
        self.nVertices = nVertices
        self.nArestas = nArestas
        self.nCores = nCores
        self.vertices = []  
        self.cores = []  
        self.idArestas = [[] for _ in range(nVertices)]  
        self.rotulos = [(0, 0) for _ in range(nVertices)]
        self.calcBase = [[[] for _ in range(nVertices)] for _ in range(nVertices)]  
        self.calcAtual = [[[] for _ in range(nVertices)] for _ in range(nVertices)] 
        self.idHistorico = []  

    def mostrarArestas(self):
        for i in self.idArestas:
            for j in i:
                print(j, end=" ")
        print("|")

def criarGrafo(instancia):
    with open(instancia, 'r') as grafoFile:
        nVertices = int(grafoFile.readline().strip())
        nCores = int(grafoFile.readline().strip())
        nArestas = int(grafoFile.readline().strip())

        grafo = Grafo(nVertices, nCores, nArestas)

        for _ in range(nVertices):
            vertice = grafoFile.readline().strip().split(',')
            if vertice[1] not in grafo.cores:
                grafo.cores.append(vertice[1])

            if not any(v.nome == vertice[0] for v in grafo.vertices):
                indiceCor = grafo.cores.index(vertice[1])
                grafo.vertices.append(Vertice(vertice[0], indiceCor))

        for _ in range(grafo.nArestas):
            aresta = grafoFile.readline().strip().split(',')

            indiceV1 = next(i for i, v in enumerate(grafo.vertices) if v.nome == aresta[0])
            indiceV2 = next(i for i, v in enumerate(grafo.vertices) if v.nome == aresta[1])

            grafo.idArestas[indiceV1].append(indiceV2)
            grafo.idArestas[indiceV2].append(indiceV1)

    return grafo