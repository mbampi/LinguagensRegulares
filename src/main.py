import os
from AFD import AFD
from GR import GR

if __name__ == '__main__':

    # Le arquivo de texto e transorma em AFD
    caminho_arquivo = os.getcwd() + '/data/AFD/exemplo.txt'
    afd = AFD.afd_de_arquivo(caminho_arquivo)
    print(afd)

    # afd.compare()

    # Dada uma lista de palavras retorna as aceitas e rejeitadas pelo AFD
    # palavras = ['a', 'ba', 'baaaa', 'aba',
    #             'ababaaa', 'ab', 'a', 'abb', 'bab', '']
    # aceitas, rejeitadas = afd.avalia_palavras(palavras)
    # print('aceita= '+str(aceitas))
    # print('rejeitadas= '+str(rejeitadas))

    # Transforma AFD em uma GR
    gr = afd.para_gramatica_regular()
    print(gr)

    caminho_gr = os.getcwd() + '/data/GR/exemploGR.txt'
    gr.gera_arquivo(caminho_gr)
