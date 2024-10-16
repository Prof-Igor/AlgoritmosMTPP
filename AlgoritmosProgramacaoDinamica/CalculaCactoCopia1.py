class Vertice:
    def __init__(self, nome, idCor):
        self.nome = nome
        self.idCor = idCor
        self.listaIdCores = []

class Grafo:
    def __init__(self, nVertices, nCores, nArestas):
        self.nVertices = nVertices
        self.nArestas = nArestas
        self.nCores = nCores
        self.vertices = []  # Lista de vértices, pode ser ajustada para o tipo Vertice quando definido
        self.cores = []  # Lista de cores (strings)
        self.idArestas = [[] for _ in range(nVertices)]  # Lista de listas para idArestas
        self.calcBase = [[[] for _ in range(nVertices)] for _ in range(nVertices)]  # Lista de tuplas para Rotulos
        self.calcAtual = [[[] for _ in range(nVertices)] for _ in range(nVertices)] 
        self.idHistorico = []  # Lista para idHistorico

def criarGrafo():
    with open('exemplo.txt', 'r') as grafoFile:
        # Lendo os dados iniciais (número de vértices, cores e arestas)
        nVertices = int(grafoFile.readline().strip())
        nCores = int(grafoFile.readline().strip())
        nArestas = int(grafoFile.readline().strip())
        grafoCores = []

        # Criando o objeto Grafo
        grafo = Grafo(nVertices, nCores, nArestas)

        # Leitura das cores e vértices
        for _ in range(nVertices):
            vertice = grafoFile.readline().strip().split(',')
            # Verificando e adicionando a cor à lista de cores
            if vertice[1] not in grafo.cores:
                grafo.cores.append(vertice[1])

            # Verificando e adicionando o vértice à lista de vértices
            if not any(v.nome == vertice[0] for v in grafo.vertices):
                indiceCor = grafo.cores.index(vertice[1])
                grafo.vertices.append(Vertice(vertice[0], indiceCor))

        # Leitura das arestas
        for _ in range(grafo.nArestas):
            aresta = grafoFile.readline().strip().split(',')

            # Encontra o índice dos vértices e adiciona às arestas correspondentes
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

def Filhos(grafo, raiz):
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

def ConjutnoCores(grafo, ciclo, inicio, fim):
    # Encontrar o índice do número inicial e final no ciclo
    idxInicio = ciclo.index(inicio)

    # Caminho pela direita (do início até o fim caminhando para frente)
    caminhoDireita = []
    i = idxInicio
    while True:
        caminhoDireita.append(grafo.vertices[ciclo[i]].idCor)
        if ciclo[i] == fim:
            break
        i = (i + 1) % len(ciclo)  # Caminha de forma circular para frente

    # Caminho pela esquerda (do início até o fim caminhando para trás)
    caminhoEsquerda = []
    i = idxInicio
    while True:
        caminhoEsquerda.append(grafo.vertices[ciclo[i]].idCor)
        if ciclo[i] == fim:
            break
        i = (i - 1) % len(ciclo)  # Caminha de forma circular para trás

    return list(set(caminhoDireita)) if len(set(caminhoDireita)) > len(set(caminhoEsquerda)) else list(set(caminhoEsquerda))

def CalculaCiclo(grafo, ant, raiz, ciclo):
    global contador
    ciclo.append(raiz)
    for v in ciclo:
        if v != raiz:
            if grafo.calcBase[raiz][v] == []:
                grafo.calcBase[raiz][v] = list(set([grafo.vertices[raiz].idCor] + ConjutnoCores(grafo, ciclo, raiz, v)))
            grafo.calcAtual[raiz][v] = list(set((grafo.calcAtual[ant][raiz] if ant is not None else []) + grafo.calcBase[raiz][v]))
            # print(f"{raiz}, {v}")
            # for j in grafo.calcAtual[raiz][v]:
            #     print(grafo.cores[j])
            # input()

def CalculaCaminho(idVertice, ant, grafo):
    # print(f"{ant} - {idVertice}")
    # print(f"{grafo.cores[grafo.vertices[ant].idCor] if ant is not None else 'None'} - {grafo.cores[grafo.vertices[idVertice].idCor]}")
    filhos = Filhos(grafo, idVertice)
    # print(filhos)
    for filhoArvore in filhos[0]:
        if grafo.calcBase[idVertice][filhoArvore] == []:
            grafo.calcBase[idVertice][filhoArvore] = list(set([grafo.vertices[idVertice].idCor , grafo.vertices[filhoArvore].idCor])) 
        
        grafo.calcAtual[idVertice][filhoArvore] = list(set((grafo.calcAtual[ant][idVertice] if ant is not None else []) + grafo.calcBase[idVertice][filhoArvore]))
        # print(f"{ant}, {idVertice}, {filhoArvore}")
        # print(f"{grafo.calcAtual[ant][idVertice] if ant is not None else []}")
        # print(grafo.calcBase[idVertice][filhoArvore])
        # print(grafo.calcAtual[idVertice][filhoArvore])
        # input()
        CalculaCaminho(filhoArvore, idVertice, grafo)
    
    for filhosCiclo in filhos[1]:
        CalculaCiclo(grafo, ant, idVertice, filhosCiclo)
        # input()
        for filhoCiclo in filhosCiclo:
            CalculaCaminho(filhoCiclo, idVertice, grafo)
    # print(f"Vertice: {grafo.vertices[idVertice].nome}, com a cor: {grafo.cores[grafo.vertices[idVertice].idCor]}")
    # grafo.idHistorico.append(idVertice)
    # for v in grafo.idArestas[idVertice]:
    #     if (v not in grafo.idHistorico):
    #         CalculaCaminho(v, grafo)

def Caminho():
    grafo = criarGrafo()

    # Filtrando os nós folha
    verticesFolha = [i for i, sublista in enumerate(grafo.idArestas) if len(sublista) == 1]
    maiorListaCores = []

    for folha in verticesFolha:
        grafo.idHistorico.append(folha)
        CalculaCaminho(folha, None, grafo)
        grafo.idHistorico = []
        for i in grafo.calcAtual:
            for j in i:
                listaAtual = [grafo.cores[k] for k in j]
                if len(listaAtual) > len(maiorListaCores):
                    maiorListaCores = listaAtual
        grafo.calcAtual = [[[] for _ in range(grafo.nVertices)] for _ in range(grafo.nVertices)]

    print(len(maiorListaCores))
    # grafo.idHistorico.append(verticesFolha[0])
    # CalculaCaminho(verticesFolha[0], None, grafo)
    # grafo.idHistorico = []
    # grafo.calcAtual = [[[] for _ in range(grafo.nVertices)] for _ in range(grafo.nVertices)]
    # grafo.idHistorico.append(verticesFolha[1])
    # CalculaCaminho(verticesFolha[1], None, grafo)
    # for i in grafo.calcBase:
    #     for j in i:
    #         for k in j:
    #             print(f"{grafo.cores[k]}", end='')
    #         print(f" | ", end='')
    #     print()

    # maior_lista = []

    # for i in grafo.calcAtual:
    #     for j in i:
    #         # Obtém a lista de cores correspondente
    #         lista_atual = [grafo.cores[k] for k in j]
            
    #         # Verifica se a lista atual é maior que a maior lista encontrada até agora
    #         if len(lista_atual) > len(maior_lista):
    #             maior_lista = lista_atual

    # # Imprime a maior lista de cores
    # print(' | '.join(maior_lista))
        
Caminho()