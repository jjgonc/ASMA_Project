import time
from spade import quit_spade
from Agents.agenteInformacao import AgenteInformacao
from Utilitarios.var import XMPP, PASSWORD, bcolors
from prettytable import PrettyTable
from Utilitarios.aviao import Aviao


def print_table(data):
        table = PrettyTable()
        num_cols = 9
        # Adiciona o cabeçalho das colunas
        table.add_column("Avião ID", [])
        table.add_column("Origem", [])
        table.add_column("Destino", [])
        table.add_column("Companhia Aérea", [])
        table.add_column("Tipo de Avião", [])
        table.add_column("Gare ID", [])
        table.add_column("Pista ID", [])
        table.add_column("Estado", [])
        table.add_column("Descrição", [])
        # Adiciona os dados
        for row in data:
            # Certifica-se de que a linha tem o número correto de colunas
            row += [''] * (num_cols - len(row))
            table.add_row(row)
        # Imprime a tabela ajustada ao tamanho do conteúdo
        table.align = 'l'
        print(table)

def print_table_ListaEspera(data):
        table = PrettyTable()
        num_cols = 6
        # Adiciona o cabeçalho das colunas
        table.add_column("Ordem de Chegada", [])
        table.add_column("Avião ID", [])
        table.add_column("Origem", [])
        table.add_column("Destino", [])
        table.add_column("Companhia Aérea", [])
        table.add_column("Tipo de Avião", [])

        # Adiciona os dados
        for row in data:
            # Certifica-se de que a linha tem o número correto de colunas
            row += [''] * (num_cols - len(row))
            table.add_row(row)
        # Imprime a tabela ajustada ao tamanho do conteúdo
        table.align = 'l'
        print(table)

def print_table_Pistas(data):
        table = PrettyTable()
        num_cols = 8
        # Adiciona o cabeçalho das colunas
        table.add_column("Pista ID", [])
        table.add_column("Localização", [])
        table.add_column("Ocupada", [])
        table.add_column("Avião ID", [])
        table.add_column("Origem", [])
        table.add_column("Destino", [])
        table.add_column("Companhia Aérea", [])
        table.add_column("Tipo de Avião", [])

        # Adiciona os dados
        for row in data:
            # Certifica-se de que a linha tem o número correto de colunas
            row += [''] * (num_cols - len(row))
            table.add_row(row)
        # Imprime a tabela ajustada ao tamanho do conteúdo
        table.align = 'l'
        print(table)


def print_table2(data):
        table = PrettyTable()
        num_cols = 6
        # Adiciona o cabeçalho das colunas
        table.add_column("Gare", [])
        table.add_column("AviaoID", [])
        table.add_column("Companhia", [])
        table.add_column("Tipo", [])
        table.add_column("Origem", [])
        table.add_column("Destino", [])
        
        # Adiciona os dados
        for row in data:
            # Certifica-se de que a linha tem o número correto de colunas
            row += [''] * (num_cols - len(row))
            table.add_row(row)
        # Imprime a tabela ajustada ao tamanho do conteúdo
        table.align = 'l'
        print(table)


def mostrarEstadoGeral(dict):
    table = []
    for k,item in dict.items():
        table.append(item.encoder())
    print_table(table)

def mostrarEstadoChegadas(dict):
    table = []
    for k,item in dict.items():
        if item.descricao == "Aterrar":
            table.append(item.encoder())
    print_table(table)

def mostrarEstadoPartidas(dict):
    table = []
    for k,item in dict.items():
        if item.descricao == "Descolar":
            table.append(item.encoder())
    print_table(table)

def mostrarEstadoListaEspera(list):
    table = []
    for i in range(0,len(list)):
        table.append([i,list[i].getID(),list[i].getOrigem(),list[i].getDestino(),list[i].getCompanhiaAerea(),list[i].getTipoAviao()])
    print_table_ListaEspera(table)
        
def mostrarEstadoPista(dict):
    table = []
    for pista in dict.values():
        if pista.getAviao() != None:
            table.append([str(pista.id),pista.loc.encoder(),pista.ocupada,pista.aviao.getID(),pista.aviao.getOrigem(),pista.aviao.getDestino(),pista.aviao.getCompanhiaAerea(),pista.aviao.getTipoAviao()])
        else:
            table.append([str(pista.id),pista.loc.encoder(),pista.ocupada,"-","-","-","-","-"])
    print_table_Pistas(table)

def mostrarHistorico(list):
    table = []
    for item in list:
        table.append(item.encoder())
    print_table(table)


def mostrarGares(dict):
    table = []
    for k,item in dict.items():
        lista = []
        if item != None :
            lista = [k , item.getID(), item.getCompanhiaAerea(), item.getTipoAviao(), item.getOrigem(), item.getDestino()]
        else :
            lista = [k, '-', '-', '-', '-', '-']
        table.append(lista)
    print_table2(table)
    
def mostrarHistoricoAviao(list,aviaoID):
    table = []
    for item in list:
        if item.aviao.getID() == aviaoID:
            table.append(item.encoder())
    print_table(table)


def menuEstado(agenteInformacao):
    print("Escolha uma opção: ")
    print("1 - Visualizar estado geral")
    print("2 - Visualizar estado das chegadas")
    print("3 - Visualizar estado das partidas")
    print("0 - Voltar Menu Principal")
    opcao = input("Opção: ")
    if opcao == "1":
        mostrarEstadoGeral(agenteInformacao.estado)
        menuEstado(agenteInformacao)
    elif opcao == "2":
        mostrarEstadoChegadas(agenteInformacao.estado)
        menuEstado(agenteInformacao)
    elif opcao == "3":
        mostrarEstadoPartidas(agenteInformacao.estado)
        menuEstado(agenteInformacao)
    elif opcao == "0":
        menuPrincipal(agenteInformacao)
    else:
        print("Opção inválida!")
        menuEstado(agenteInformacao)


def menuHistorico(agenteInformacao):
    print("Escolha uma opção: ")
    print("1 - Visualizar histórico geral")
    print("2 - Visualizar histórico de um aviao")
    print("0 - Voltar Menu Principal")
    opcao = input("Opção: ")
    if opcao == "1":
        mostrarHistorico(agenteInformacao.historico)
        menuHistorico(agenteInformacao)
    elif opcao == "2":
        aviaoID = input("Introduza o id do aviao: ")
        mostrarHistoricoAviao(agenteInformacao.historico,aviaoID)
        menuHistorico(agenteInformacao)
    elif opcao == "0":
        menuPrincipal(agenteInformacao)
    else:
        print("Opção inválida!")
        menuHistorico(agenteInformacao)


def menuPrincipal(agenteInformacao):
    print("Escolha uma opção: ")
    print("1 - Visualizar estado atual")
    print("2 - Visualizar histórico")
    print("3 - Visualizar Gares")
    print("4 - Visualizar Listas de Espera")
    print("5 - Visualizar Pistas")
    print("6 - Sair")
    opcao = input("Opção: ")
    if opcao == "1":
        menuEstado(agenteInformacao)
    elif opcao == "2":
        menuHistorico(agenteInformacao)
    elif opcao == '3':
        mostrarGares(agenteInformacao.gares)
        menuPrincipal(agenteInformacao)
    elif opcao == "4":
        print(bcolors.FAIL + "\t\t\tAterrar" + bcolors.ENDC)
        mostrarEstadoListaEspera(agenteInformacao.listaEsperaAterrar)
        print(bcolors.FAIL +"\t\t\tDescolar"+ bcolors.ENDC)
        mostrarEstadoListaEspera(agenteInformacao.listaEsperaDescolar)
        menuPrincipal(agenteInformacao)
    elif opcao == "5":
        mostrarEstadoPista(agenteInformacao.pistas)
        menuPrincipal(agenteInformacao)
    elif opcao == '6':
        agenteInformacao.stop()
    else:
        print("Opção inválida!")
        menuPrincipal(agenteInformacao)
    

def main():
    agenteInformacao = AgenteInformacao("agenteInformacao"+XMPP, PASSWORD)
    futureA = agenteInformacao.start()
    futureA.result()

    menuPrincipal(agenteInformacao)

    print(bcolors.BOLD + 'Agents finished' + bcolors.ENDC)

    quit_spade()


if __name__ == '__main__':
    main()