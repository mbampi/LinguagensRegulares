
import re
import pandas as pd
from GR import GR


class AFD:

    def __init__(self, nome=None, estados=[], simbolos=[], estado_inicial=None, estados_finais=[], funcoes_programa={}):
        self.nome = nome
        self.estados = estados
        self.simbolos = simbolos
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais
        self.funcoes_programa = funcoes_programa

    @staticmethod
    def afd_de_arquivo(caminho_arquivo):
        ''' Le um arquivo dado pelo caminho especificado e
        retorna um automato finito deterministico'''

        with open(caminho_arquivo) as file:
            first_line = file.readline().split("=", 1)

            nome = first_line[0]

            # retira parenteses
            str_definicao = first_line[1][1:-1]
            # troca '{}' por '()'
            str_definicao = str_definicao.replace(
                '{', '(').replace('}', ')')

            # regex para achar elementos entre ',' ou conjuntos de elementos entre '{}'
            regex_exp = "[^,()]*(?:\([^)]*\))*[^,]*"
            definicao = re.findall(regex_exp, str_definicao)

            # tira os '()' e tira espacos em branco
            definicao = [i.strip().replace('(', '').replace(')', '')
                         for i in definicao if i]
            # separa string pelas ','
            definicao = [i.split(',') for i in definicao]

            estados = definicao[0]
            simbolos = definicao[1]
            estado_inicial = definicao[2][0]
            estados_finais = definicao[3]

            # descarta linha 'Prog'
            file.readline()

            funcoes_programa = {}
            for line in file.readlines():
                estado = re.search('^\((.*),', line)[0][1: -1]
                simbolo = re.search(',(.*)\)=', line)[0][1: -2]
                estado_resultante = re.search('=(.*)$', line)[0][1:]

                funcoes_programa[(estado, simbolo)] = estado_resultante

            return AFD(nome, estados, simbolos, estado_inicial, estados_finais, funcoes_programa)

    def __str__(self):
        output = f'\nnome={self.nome}'
        output += f'\nestados={self.estados}'
        output += f'\nsimbolos={self.simbolos}'
        output += f'\nestado_inicial={self.estado_inicial}'
        output += f'\nestados_finais={self.estados_finais}'
        output += f'\nfuncoes_programa='
        output += str([str(fp) + ' -> ' + str(e) for fp,
                       e in self.funcoes_programa.items()])
        return output

    def saida(self, estado, simbolo):
        ''' Dado um estado e um simbolo,
        retorna o seu estado resultante 
        a partir das funcoes programas do AFD'''
        funcao_programa = (estado, simbolo)
        for fp, resultante in self.funcoes_programa.items():
            if fp == funcao_programa:
                return str(resultante)
        return None

    def aceita(self, palavra):
        ''' Dada uma palavra, retorna True se ela eh aceita pelo AFD,
        ou False caso nao seja'''
        estado_atual = self.estado_inicial
        for simbolo in palavra:
            resultante = self.saida(estado_atual, simbolo)
            if resultante == None:
                return False
            else:
                estado_atual = resultante

        return (estado_atual in self.estados_finais)

    def avalia_palavras(self, palavras):
        ''' Dada uma lista de palavras, retorna uma tupla de listas:
        "aceita" eh a lista de palavras aceitas pelo AFD
        "rejeita" eh a lista de palavras rejeitadas pelo AFD'''
        aceita = []
        rejeita = []
        for palavra in palavras:
            if self.aceita(palavra):
                aceita.append(palavra)
            else:
                rejeita.append(palavra)
        return aceita, rejeita

    def para_gramatica_regular(self):
        ''' Gera a gramatica regular (GR) equivalente
        a partir do AFD'''
        # deixa o estado inicial em primeiro da lista
        index_estado_inicial = self.estados.index(self.estado_inicial)
        self.estados[0], self.estados[index_estado_inicial] = self.estados[index_estado_inicial], self.estados[0]

        producoes = {}
        for estado in self.estados:
            producoes[estado] = []
            for simbolo in self.simbolos:
                prod = self.saida(estado, simbolo)
                if prod:
                    producoes[estado].append(simbolo + " " + prod)

        for estado_final in self.estados_finais:
            if producoes.get(estado_final):
                producoes[estado_final].append(' ')
            else:
                producoes[estado_final] = ' '

        return GR(nome=self.nome, variaveis=self.estados, terminais=self.simbolos, producoes=producoes, variavel_inicial=self.estado_inicial)

    def minimizado(self):
        dicAux = {}
        for st_a in range(len(self.estados)):
            for st_b in range(st_a+1, len(self.estados)):
                '''
                    True não está marcado
                    False está marcado
                '''
                if self.estados[st_a] in self.estados_finais:
                    if self.estados[st_b] in self.estados_finais:
                        dicAux[(self.estados[st_a], self.estados[st_b])] = True
                    else:
                        dicAux[(self.estados[st_a], self.estados[st_b])] = False
                else:
                    if self.estados[st_b] in self.estados_finais:
                        dicAux[(self.estados[st_a], self.estados[st_b])] = False
                    else:
                        dicAux[(self.estados[st_a], self.estados[st_b])] = True

                # if self.estados[st_a] == 'QV' or self.estados[st_b] == 'QV':
                    # dicAux[(self.estados[st_a], self.estados[st_b])] = False
        '''
            Verifica se os estados são equivalentes
            apos realizar os laços
            se a relação de estados no variavel dic ainda for True
            quer dizer que aqueles dois estados são equivalentes e podem ser juntados
        '''
        for st_a in range(len(self.estados)):
            for st_b in range(st_a+1, len(self.estados)):
                if dicAux[(self.estados[st_a], self.estados[st_b])]:
                    for simb in range(len(self.simbolos)):
                        aux_a = self.funcoes_programa[(
                            self.estados[st_a], self.simbolos[simb])]
                        aux_b = self.funcoes_programa[(
                            self.estados[st_b], self.simbolos[simb])]
                        if aux_a == aux_b:
                            break
                        else:
                            if (aux_a, aux_b) in dicAux:
                                dicAux[(self.estados[st_a], self.estados[st_b])] = dicAux[(
                                    aux_a, aux_b)]
                            else:
                                dicAux[(self.estados[st_a], self.estados[st_b])] = dicAux[(
                                    aux_b, aux_a)]
        listRemoveSt = []
        for st_a in range(len(self.estados)):
            for st_b in range(st_a+1, len(self.estados)):
                if dicAux.get((self.estados[st_a], self.estados[st_b])):
                    # Cria o novo estado
                    st_novo = self.estados[st_a]+self.estados[st_b]
                    self.estados.append(st_novo)
                    # remove os estados equivalentes da lista de estados
                    st_removeA = self.estados[st_a]
                    st_removeB = self.estados[st_b]
                    listRemoveSt.append(st_removeA)
                    listRemoveSt.append(st_removeB)
                    # Verifica se os estados são finais, se sim remove da lista de estados finais e cria o novo estado
                    if st_removeA in self.estados_finais:
                        self.estados_finais.remove(st_removeA)
                        self.estados_finais.remove(st_removeB)
                        if st_novo not in self.estados_finais:
                            self.estados_finais.append(st_novo)

                    for simb in self.simbolos:
                        keyNew = (st_novo, simb)
                        keyA = (st_removeA, simb)
                        keyB = (st_removeB, simb)
                        if keyA in self.funcoes_programa:
                            if keyNew not in self.funcoes_programa:
                                self.funcoes_programa[keyNew] = self.funcoes_programa[keyA]
                            del self.funcoes_programa[keyA]
                        if keyB in self.funcoes_programa:
                            del self.funcoes_programa[keyB]
        for st in list(set(listRemoveSt)):
            self.estados.remove(st)

    def eh_equivalente(self, afd):
        ''' Determina se os dois AFD's sao equivalentes
        minimizando os dois e comparando eles posteriormente 
        (AFD minimo eh unico)'''
        afd1 = self.minimizado()
        afd2 = afd2.minimizado()
        # AFD minimizados sao unicos
        # depois de minimizado
        # renomear os estados e terminais
        # comparar se sao iguais

    def equaivalencia_de_estados(self):
        pass
        table = pd.DataFrame(columns=self.estados[:-1], index=self.estados[1:])
        print(table.loc['Q1', 'Q2'])

    def funcao_programa_total(self):
        # QV eh o estado vazio
        flag = False
        for estado in self.estados:
            for simbolo in self.simbolos:
                fp = self.funcoes_programa.get((estado, simbolo))
                if not fp:
                    self.funcoes_programa[(estado, simbolo)] = 'QV'
                    flag = True
        if flag:
            self.estados.append('QV')
            for simb in self.simbolos:
                self.funcoes_programa[('QV', simb)] = 'QV'
