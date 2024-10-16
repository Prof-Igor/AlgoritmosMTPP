import time

class Vertice:
    def __init__(self, nome, idCor):
        self.nome = nome
        self.idCor = idCor

class Grafo:
    def __init__(self, nVertices, nCores, nArestas):
        self.nVertices = nVertices
        self.nArestas = nArestas
        self.nCores = nCores
        self.vertices = []  
        self.cores = []  
        self.idArestas = [[] for _ in range(nVertices)]  
        self.calcBase = [[[] for _ in range(nVertices)] for _ in range(nVertices)]  
        self.calcAtual = [[[] for _ in range(nVertices)] for _ in range(nVertices)] 
        self.idHistorico = []  

def criarGrafo():
    with open('Instancias/Exemplo 1.txt', 'r') as grafoFile:
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

def verificaCiclo(grafo, u, ciclo, ant, historico):
    if u in ciclo:
        return ciclo

    for filho in grafo.idArestas[ciclo[-1]]:
        if u in ciclo:
            return ciclo
        elif filho == ant:
            continue
        elif filho in historico:
            break

        ciclo.append(filho)
        historico.append(filho)
        verificaCiclo(grafo, u, ciclo, ciclo[-2], historico)

    if u in ciclo:
        return ciclo
    else:
        ciclo.pop()
        return ciclo

def buscaFilhos(grafo, raiz):
    filhos_arvore = []
    filhos_ciclo = []

    for filho in grafo.idArestas[raiz]:
        if filho not in grafo.idHistorico:
            ciclo = [filho]
            historico = [filho]
            verificaCiclo(grafo, raiz, ciclo, raiz, historico)
            
            if len(ciclo) == 0:
                filhos_arvore.append(filho)
                grafo.idHistorico.append(filho)
            else:
                ciclo.pop()
                lista_ciclo = []
                for nos in ciclo:
                    lista_ciclo.append(nos)
                    grafo.idHistorico.append(nos)
                filhos_ciclo.append(lista_ciclo)

    for i in range(len(filhos_ciclo)):
        for j in range(len(filhos_ciclo)):
            if (filhos_ciclo[i][0] == filhos_ciclo[j][-1] and
                filhos_ciclo[i][-1] == filhos_ciclo[j][0]):
                filhos_ciclo.pop(j)

    return filhos_arvore, filhos_ciclo

def conjuntoCores(grafo, ciclo, inicio, fim):
    idxInicio = ciclo.index(inicio)

    caminhoDireita = []
    i = idxInicio
    while True:
        caminhoDireita.append(grafo.vertices[ciclo[i]].idCor)
        if ciclo[i] == fim:
            break
        i = (i + 1) % len(ciclo)

    caminhoEsquerda = []
    i = idxInicio
    while True:
        caminhoEsquerda.append(grafo.vertices[ciclo[i]].idCor)
        if ciclo[i] == fim:
            break
        i = (i - 1) % len(ciclo)

    return list(set(caminhoDireita)) if len(set(caminhoDireita)) > len(set(caminhoEsquerda)) else list(set(caminhoEsquerda))

def calculaCaminho(idVertice, ant, grafo):
    filhos = buscaFilhos(grafo, idVertice)

    for filhoArvore in filhos[0]:
        if grafo.calcBase[idVertice][filhoArvore] == []:
            grafo.calcBase[idVertice][filhoArvore] = list(set([grafo.vertices[idVertice].idCor , grafo.vertices[filhoArvore].idCor])) 
        
        grafo.calcAtual[idVertice][filhoArvore] = list(set((grafo.calcAtual[ant][idVertice] if ant is not None else []) + grafo.calcBase[idVertice][filhoArvore]))

        calculaCaminho(filhoArvore, idVertice, grafo)
    
    for filhosCiclo in filhos[1]:
        filhosCiclo.append(idVertice)
        for v in filhosCiclo:
            if v != idVertice:
                if grafo.calcBase[idVertice][v] == []:
                    grafo.calcBase[idVertice][v] = list(set([grafo.vertices[idVertice].idCor] + conjuntoCores(grafo, filhosCiclo, idVertice, v)))
                grafo.calcAtual[idVertice][v] = list(set((grafo.calcAtual[ant][idVertice] if ant is not None else []) + grafo.calcBase[idVertice][v]))

        for filhoCiclo in filhosCiclo:
            calculaCaminho(filhoCiclo, idVertice, grafo)

def calculaCacto(grafo):
    verticesFolha = [i for i, sublista in enumerate(grafo.idArestas) if len(sublista) == 1]
    maiorListaCores = []

    tempoInicial = time.time()

    for folha in verticesFolha:
        grafo.idHistorico.append(folha)
        calculaCaminho(folha, None, grafo)
        grafo.idHistorico = []
        for i in grafo.calcAtual:
            for j in i:
                listaAtual = [grafo.cores[k] for k in j]
                if len(listaAtual) > len(maiorListaCores):
                    maiorListaCores = listaAtual
        grafo.calcAtual = [[[] for _ in range(grafo.nVertices)] for _ in range(grafo.nVertices)]
    
    tempoFinal = time.time()
    tempoExecucao = tempoFinal - tempoInicial
    return len(maiorListaCores), tempoExecucao
