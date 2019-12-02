import os
import csv

from AFD import AFD
from GR import GR


def csv_para_lista(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        leitor = csv.reader(arquivo)
        lista = list(leitor)[0]
    return lista


if __name__ == '__main__':

    # Le arquivo de texto e transorma em AFD
    caminho_arquivo = os.getcwd() + '/data/AFD/exemplo.txt'
    afd = AFD.afd_de_arquivo(caminho_arquivo)
    print(afd)

    # Dada uma lista de palavras retorna as aceitas e rejeitadas pelo AFD
    caminho_palavras = os.getcwd() + '/data/Palavras/teste.csv'
    palavras = csv_para_lista(caminho_palavras)
    print(palavras)
    # palavras = ['a', 'ba', 'baaaa', 'aba',
    #             'ababaaa', 'ab', 'a', 'abb', 'bab', '']
    aceitas, rejeitadas = afd.avalia_palavras(palavras)
    print('aceitas= '+str(aceitas))
    print('rejeitadas= '+str(rejeitadas))

    # Transforma AFD em uma GR
    gr = afd.para_gramatica_regular()
    print(gr)

    caminho_gr = os.getcwd() + '/data/GR/exemploGR.txt'
    gr.gera_arquivo(caminho_gr)
