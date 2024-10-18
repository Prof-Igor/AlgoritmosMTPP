class Grafo:
    def __init__(self, nVertices):
        self.nVertices = nVertices
        self.calcBase = [[[] for _ in range(nVertices)] for _ in range(nVertices)]  
        self.calcAtual = [[[] for _ in range(nVertices)] for _ in range(nVertices)] 

maiorListaCores = []

grafo = Grafo(100)

for i in grafo.calcAtual:
    for j in i:
        for k in j:
            print(k)
