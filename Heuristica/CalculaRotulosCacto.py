import time

def EFolha(G, u):
    for item in G.idArestas[u]:
        if item not in G.idHistorico:
            return False
    return True

def VerificaCiclo(G, u, ciclo, ant, historico):
    if u in ciclo:
        return ciclo

    for filho in G.idArestas[ciclo[-1]]:  # ciclo.Last() em C# é ciclo[-1] em Python
        if u in ciclo:
            return ciclo
        elif filho == ant:
            continue
        elif filho in historico:
            break

        ciclo.append(filho)
        historico.append(filho)
        VerificaCiclo(G, u, ciclo, ciclo[-2], historico)  # ciclo[ciclo.Count - 2] é ciclo[-2]

    if u in ciclo:
        return ciclo
    else:
        ciclo.pop()  # RemoveAt em C# é pop() em Python
        return ciclo

def Filhos(G, u):
    filhosArvore = []
    filhosCiclo = []

    for filho in G.idArestas[u]:
        if filho not in G.idHistorico:
            ciclo = [filho]
            historico = [filho]
            VerificaCiclo(G, u, ciclo, u, historico)

            if len(ciclo) == 0:
                filhosArvore.append(filho)
                G.idHistorico.append(filho)
            else:
                ciclo.pop()
                listaCiclo = []
                for nos in ciclo:
                    listaCiclo.append(nos)
                    G.idHistorico.append(nos)
                filhosCiclo.append(listaCiclo)

    for i in range(len(filhosCiclo)):
        for j in range(len(filhosCiclo)):
            if (filhosCiclo[i][0] == filhosCiclo[j][-1] and 
                filhosCiclo[i][-1] == filhosCiclo[j][0]):
                filhosCiclo.pop(j)

    return filhosArvore, filhosCiclo

def Sequencia(G, ciclo, sequencia, melhorVertice):
    for item in G.idArestas[sequencia[-1]]:  # sequencia.Last() em C# é sequencia[-1] em Python
        if item in ciclo and item not in sequencia and item != melhorVertice:
            sequencia.append(item)
            Sequencia(G, ciclo, sequencia, melhorVertice)
    return sequencia


def Aux(G, ciclo, Pai):
    ConjuntosCores = []

    for item in ciclo:
        vizinhos = [vert for vert in G.idArestas[item] if vert in ciclo]

        if len(vizinhos) == 1:
            CoresCiclo = list(G.vertices[item].idCores)

            for vert in ciclo:
                if G.vertices[vert].idCor not in CoresCiclo:
                    CoresCiclo.append(G.vertices[vert].idCor)

            if G.vertices[Pai].idCor not in CoresCiclo:
                CoresCiclo.append(G.vertices[Pai].idCor)

            ConjuntosCores.append(CoresCiclo)
        else:
            SequenciaA = [vizinhos[0]]
            Sequencia(G, ciclo, SequenciaA, item)

            CoresLadoA = list(G.vertices[item].idCores)

            for vert in SequenciaA:
                if G.vertices[vert].idCor not in CoresLadoA:
                    CoresLadoA.append(G.vertices[vert].idCor)

            if G.vertices[Pai].idCor not in CoresLadoA:
                CoresLadoA.append(G.vertices[Pai].idCor)

            ConjuntosCores.append(CoresLadoA)

            SequenciaB = [vizinhos[1]]
            Sequencia(G, ciclo, SequenciaB, item)

            CoresLadoB = list(G.vertices[item].idCores)

            for vert in SequenciaB:
                if G.vertices[vert].idCor not in CoresLadoB:
                    CoresLadoB.append(G.vertices[vert].idCor)

            if G.vertices[Pai].idCor not in CoresLadoB:
                CoresLadoB.append(G.vertices[Pai].idCor)

            ConjuntosCores.append(CoresLadoB)

    return max(ConjuntosCores, key=len)


def MelhoresFilhos(CoresFilhos):
    Melhores = list(CoresFilhos[0])  # Copia os elementos da primeira lista
    
    for i in range(len(CoresFilhos)):
        for j in range(i + 1, len(CoresFilhos)):
            Atual = list(CoresFilhos[i])  # Copia a lista atual
            for item in CoresFilhos[j]:
                if item not in Atual:
                    Atual.append(item)

            if len(Atual) > len(Melhores):
                Melhores = Atual

    return len(Melhores)

def computarCores(G, u):
    if EFolha(G, u):
        G.rotulos[u] = (1, 1)  # Usando uma tupla comum em Python
        if G.vertices[u].idCor not in G.vertices[u].idCores:
            G.vertices[u].idCores.append(G.vertices[u].idCor)
    else:
        filhos = Filhos(G, u)  # Retorna uma tupla de lista de filhos e lista de ciclos
        CoresFilhos = []

        for raiz in filhos[0]:
            computarCores(G, raiz)
            CoresFilhos.append(list(set(G.vertices[raiz].idCores)))  # Distinct em Python é set()
            if G.vertices[u].idCor not in CoresFilhos[-1]:
                CoresFilhos[-1].append(G.vertices[u].idCor)

        for ciclos in filhos[1]:
            for raiz in ciclos:
                computarCores(G, raiz)
            CoresFilhos.append(list(set(Aux(G, ciclos, u))))  # Distinct em Python é set()

        MaiorCores = max(CoresFilhos, key=len)  # Usando max para encontrar a lista com mais cores
        G.rotulos[u] = (len(MaiorCores), MelhoresFilhos(CoresFilhos))
        for item in set(MaiorCores):  # Distinct é set()
            if item not in G.vertices[u].idCores:
                G.vertices[u].idCores.append(item)

def computaCores(grafo):
    max = 0

    tempoInicial = time.time()

    for j in range(grafo.nVertices):
        grafo.idHistorico.clear()
        for k in range(len(grafo.vertices)):
            grafo.rotulos[k] = (0, 0)
            grafo.vertices[k].idCores.clear()
        grafo.idHistorico.append(j)
        computarCores(grafo, j)
        for item in grafo.rotulos:
            if item[1] > max:  # Acessando o segundo item da tupla com índice 1
                max = item[1]
        if max == grafo.nCores:
            break

    tempoFinal = time.time()
    tempoExecucao = tempoFinal - tempoInicial
    return max, tempoExecucao