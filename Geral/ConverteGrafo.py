from .Grafo import Grafo

def verificaCiclo(G, ini, v, ciclo, historico):
    if len(set(G.idArestas[v]) - set(G.idHistorico)) == 0:
        return ciclo

    for filho in G.idArestas[v]:
        if filho not in historico:
            if G.vertices[ini] in ciclo[0]:
                return ciclo
            if filho not in G.idHistorico and G.vertices[filho] not in ciclo[0] and filho != ini:
                ciclo[0].append(G.vertices[filho])
                historico.append(filho)
                ciclo[1].append((v, filho))
                ciclo[1].append((filho, v))

                verificaCiclo(G, ini, filho, ciclo, historico)

                if ciclo[0][-1] == G.vertices[filho]:
                    ciclo[0].pop()
            elif len(ciclo[0]) >= 2 and G.vertices[filho] not in ciclo[0]:
                ciclo[0].append(G.vertices[filho])
                historico.append(filho)
                if G.vertices[ini] in ciclo[0]:
                    ciclo[1].append((v, filho))
                    ciclo[1].append((filho, v))
                    return ciclo
                ciclo[0].pop()
    return ciclo

def adaptarGrafo(G, G2, v):
    cicloCompleto = verificaCiclo(G, v, v, ([], []), [])

    if len(cicloCompleto[0]) > 2:
        for item in cicloCompleto[0]:
            if item != G.vertices[v]:
                G.idHistorico.append(G.vertices.index(item))
                G2.vertices.append(item)
        for item in cicloCompleto[1]:
            if G.vertices[item[0]] in G2.vertices and G.vertices[item[1]] in G2.vertices:
                G2.idArestas[G2.vertices.index(G.vertices[item[0]])].append(G2.vertices.index(G.vertices[item[1]]))
        for item in G.vertices:
            if G.vertices.index(item) not in G.idHistorico:
                for item2 in cicloCompleto[0]:
                    if G.vertices.index(item) not in G.idHistorico:
                        if G.vertices.index(item) in G.idArestas[G.vertices.index(item2)]:
                            G.idHistorico.append(G.vertices.index(item))
                            G2.vertices.append(item)
                            G2.idArestas[G2.vertices.index(item)].append(G2.vertices.index(item2))
                            G2.idArestas[G2.vertices.index(item2)].append(G2.vertices.index(item))
                            if len(G2.vertices) - len(G.vertices) != 0:
                                adaptarGrafo(G, G2, G.vertices.index(item))
    else:
        for item in G.idArestas[v]:
            if item not in G.idHistorico:
                G.idHistorico.append(item)
                G2.vertices.append(G.vertices[item])
                G2.idArestas[G2.vertices.index(G2.vertices[0])].append(G2.vertices.index(G.vertices[item]))
                G2.idArestas[G2.vertices.index(G.vertices[item])].append(G2.vertices.index(G2.vertices[0]))
                if len(G2.vertices) - len(G.vertices) != 0:
                    adaptarGrafo(G, G2, item)

def adaptaGrafo(G):
    G2 = Grafo(G.nVertices, G.nCores, G.nArestas)
    G2.vertices.append(G.vertices[0])
    G2.cores = G.cores

    G.idHistorico.append(0)
    adaptarGrafo(G, G2, 0)
    return G2