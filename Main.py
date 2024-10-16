from Geral.Grafo import criarGrafo
from Geral.ConverteGrafo import adaptaGrafo
from AlgoritmosProgramacaoDinamica.CalculaCacto import calculaCacto
from Heuristica.CalculaRotulosCacto import computaCores

print("Seja bem vindo ao sistema de algoritmos para o Problema do Caminho Tropical Máximo MTPP, desenvolvido por Igor de Moraes Sampaio!")

def executarAlgoritmo(grafo, algoritmo, adaptar):
    if adaptar == "1":
        grafoAdaptado = adaptaGrafo(grafo)
    else:
        grafoAdaptado = grafo

    if algoritmo == "1":
        return computaCores(grafoAdaptado)
    elif algoritmo == "2":
        return calculaCacto(grafoAdaptado)

def processarInstancias(algoritmoEscolhido, adaptar):
    arquivoInstancias = 'Instancias/MTPP/nomes.txt' if adaptar == "1" else 'Instancias/Cacto/nomes.txt'

    with open(arquivoInstancias, 'r') as instancias:
        numInstancias = int(instancias.readline().strip())
        
        for _ in range(numInstancias):
            nomeGrafo = instancias.readline().strip()
            arquivoInstancia = f'Instancias/MTPP/{nomeGrafo}.txt' if adaptar == "1" else f'Instancias/Cacto/{nomeGrafo}.txt'
            grafo = criarGrafo(arquivoInstancia)
            resposta, tempoExecucao = executarAlgoritmo(grafo, algoritmoEscolhido, adaptar)
            print(f"Resposta: {resposta} cores")
            print(f'Tempo de execução: {tempoExecucao:.20f} segundos')

def main():
    while True:
        algoritmoEscolhido = input("Escolha o algoritmo você que executar: \n 1 - Heurística \n 2 - Programação Dinamica \n 0 - Sair \n Digite a opção: ")
        if algoritmoEscolhido in ["1", "2"]:
            adaptar = input("Executar quais instancias: \n 1 - Grafos \n 2 - Grafos Cactos \n 3 - Voltar \n 0 = Sair \n Digite a opção: ")
            if adaptar in ["1", "2"]:
                processarInstancias(algoritmoEscolhido, adaptar)
                break
            elif adaptar == "3":
                continue
            else:
                print("Valor selecionado é inválido! Tente novamente!")
        elif algoritmoEscolhido == "0":
            print("Saindo do sistema.")
            break
        else:
            print("Valor selecionado é inválido! Tente novamente!")

if __name__ == "__main__":
    main()