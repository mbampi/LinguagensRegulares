import os
import csv

from AFD import AFD
from AFN import AFN
from GR import GR


def csv_para_lista(caminho_arquivo):
    palavras = []
    with open(caminho_arquivo, 'r') as arquivo:
        leitor = csv.reader(arquivo)
        for linha in leitor:
            palavras.append(list(linha))
    return palavras


def le_afn_e_transforma_para_afd():
    caminho_arquivo = os.getcwd() + '/data/AFN/tpoint.txt'
    afn = AFN.afn_de_arquivo(caminho_arquivo)
    print(afn)

    afd = afn.para_AFD()
    return afd


def le_afd_e_deixa_fp_total():
    # ---- Le arquivo de texto e transorma em AFD ----
    caminho_arquivo = os.getcwd() + '/data/AFD/exemplo.txt'
    afd = AFD.afd_de_arquivo(caminho_arquivo)
    print(afd)

    afd.funcao_programa_total()
    print(afd)


def le_lista_palavras_e_avalia(afd):
    # ---- Dada uma lista de palavras retorna as aceitas e rejeitadas pelo AFD ----
    caminho_palavras = os.getcwd() + '/data/Palavras/teste.csv'
    palavras = csv_para_lista(caminho_palavras)
    aceitas, rejeitadas = afd.avalia_palavras(palavras)
    print('aceitas= '+str(aceitas))
    print('rejeitadas= '+str(rejeitadas))


def compara_automatos():
    caminho_arquivo = os.getcwd() + '/data/AFD/exemplo.txt'
    afd1 = AFD.afd_de_arquivo(caminho_arquivo)

    caminho_arquivo = os.getcwd() + '/data/AFD/exemplo.txt'
    afd2 = AFD.afd_de_arquivo(caminho_arquivo)

    print(afd1.eh_equivalente(afd2))


def gera_gr(afd):
    # ---- Transforma AFD em uma GR ----
    caminho_gr = os.getcwd() + '/data/GR/exemploGR.txt'
    gr = afd.para_gramatica_regular()
    gr.gera_arquivo(caminho_gr)
    print(gr)


if __name__ == '__main__':
    compara_automatos()
