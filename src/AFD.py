
import re
import pandas as pd
from itertools import product

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

    @staticmethod
    def copy(afd):
        return AFD(nome=afd.nome, estados=afd.estados, simbolos=afd.simbolos, estado_inicial=afd.estado_inicial, estados_finais=afd.estados_finais, funcoes_programa=afd.funcoes_programa)

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

    def aceita(self, palavra):
        ''' Dada uma palavra, retorna True se ela eh aceita pelo AFD,
        ou False caso nao seja'''
        estado_atual = self.estado_inicial
        for simbolo in palavra:
            resultante = self.funcoes_programa.get((estado_atual, simbolo))
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
                prod = self.funcoes_programa.get((estado, simbolo))
                if prod:
                    producoes[estado].append(simbolo + " " + prod)

        for estado_final in self.estados_finais:
            if producoes.get(estado_final):
                producoes[estado_final].append(' ')
            else:
                producoes[estado_final] = ' '

        return GR(nome=self.nome, variaveis=self.estados, terminais=self.simbolos, producoes=producoes, variavel_inicial=self.estado_inicial)

    def funcao_programa_total(self):
        # QV eh o estado vazio desintado a receber
        for estado in self.estados:
            for simbolo in self.simbolos:
                fp = self.funcoes_programa.get((estado, simbolo))
                if not fp:
                    self.funcoes_programa[(estado, simbolo)] = 'QV'

    def minimizado(self):
        tabSt = {}
        '''
            Cria uma tabela de todos os pares de estados (Qi, Qj) todos desmarcados inicialmente ( {(Qi, Qj) : True} )
        '''
        for a in range(len(self.estados)):
            for b in range(a+1, len(self.estados)):
                st_a = self.estados[a]
                st_b = self.estados[b]
                tabSt[(st_a, st_b)] = True
        '''
            Percorre a tabela e marca {(Qi, Qj) : False} os pares de estados (Qi, Qj) onde Qi ∈ F e Qj ∉ F, ou vice-versa
        '''
        for ka, kb in tabSt:
            if (ka in self.estados_finais) and (kb not in self.estados_finais):
                tabSt[(ka, kb)] = False
            elif (kb in self.estados_finais) and (ka not in self.estados_finais):
                tabSt[(ka, kb)] = False
        '''
            Fica repetindo o processo até não ter mais novas marcações:
            se houver um par não marcado (Qi, Qj), marque-o se o par {δ(Qi, S), δ(Qi, S)} estiver marcado para qualquer alfabeto de entrada (S)
        '''
        marcou = True
        while(marcou):
            for ka, kb in tabSt:
                marcou = False
                if tabSt[(ka, kb)]:
                    for s in self.simbolos:
                        st_ka = (ka, s)
                        st_kb = (kb, s)
                        if st_ka not in self.funcoes_programa:
                            tabSt[(ka, kb)] = False
                            marcou = True
                        elif st_kb not in self.funcoes_programa:
                            tabSt[(ka, kb)] = False
                            marcou = True
                        else:
                            st_ra = self.funcoes_programa[st_ka]
                            st_rb = self.funcoes_programa[st_kb]
                            a = (st_ra, st_rb)
                            b = (st_rb, st_rb)
                            if a in tabSt:
                                if not tabSt[a]:
                                    tabSt[(ka, kb)] = False
                                    marcou = True
                            if b in tabSt:
                                if not tabSt[b]:
                                    tabSt[(ka, kb)] = False
                                    marcou = True
        '''
            Cria duas listas auxiliares, sendo que elas tem o seguinte proposito:
            listStEq - É uma lista de lista, onde na lista filho vai ter a lista de estados equivalente.
            stPassados - É uma lista que informa quais são os estados que foram salvos na listStEq para
                facilitar a remoção desses estados unicos e assim substitui-los por novo estado que
                unifica todos os estados equivalentes
        '''
        listStEq = []
        stPassados = []
        for ka, kb in tabSt:
            if tabSt[(ka, kb)]:
                if not listStEq:
                    listStEq.append([ka, kb])
                    stPassados.append(ka)
                    stPassados.append(kb)
                else:
                    if ka in stPassados:
                        for x in listStEq:
                            if ka in x and kb not in x:
                                x.append(kb)
                                stPassados.append(kb)
                    elif kb in stPassados:
                        for x in listStEq:
                            if kb in x and ka not in x:
                                x.append(ka)
                                stPassados.append(ka)
                    else:
                        listStEq.append([ka, kb])
                        stPassados.append(ka)
                        stPassados.append(kb)
        '''
            Cria o novo estado, que unifica todos os estados equivalente, e remove os setados unicos
        '''
        for x in listStEq:
            stPassados = []
            stNew = ''
            for y in x:
                stNew = stNew+y
                stPassados.append(y)
            self.estados.append(stNew)
            for stRemove in stPassados:
                if stRemove in self.estados:
                    self.estados.remove(stRemove)
                if stRemove == self.estado_inicial:
                    self.estado_inicial = stNew
                if stRemove in self.estados_finais:
                    if stNew not in self.estados_finais:
                        self.estados_finais.append(stNew)
                    self.estados_finais.remove(stRemove)
                for s in self.simbolos:
                    if (stRemove, s) in self.funcoes_programa:
                        if (stNew, s) not in self.funcoes_programa:
                            a = self.funcoes_programa[(stRemove, s)]
                            self.funcoes_programa[(stNew, s)] = a
                        del self.funcoes_programa[(stRemove, s)]

        tabela = pd.DataFrame(
            columns=self.estados[:-1], index=self.estados[1:])
        for y in range(1, len(self.estados)-1):
            for x in range(0, y-1):
                print(tabela.iloc[y])
            print('/n')

    @staticmethod
    def combinacoes(lista, tamanho):
        ''' Gera combinacao dos elementos da lista de 1 
        ate o 'tamanho', retorna uma lista de listas'''
        todas_palavras = []
        for tam in range(1, tamanho+1):
            lista_palavras = list(product(lista, repeat=tam))
            palavras = list(map(lambda a: list(a), lista_palavras))
            todas_palavras.extend(palavras)

        return todas_palavras

    def eh_equivalente(self, afd):
        ''' Determina se os dois AFD's sao equivalentes
        minimizando os dois e comparando eles posteriormente
        (AFD minimo eh unico)'''
        afd1 = AFD.copy(self)
        afd2 = afd
        afd1.minimizado()
        afd2.minimizado()
        if len(afd1.estados) != len(afd2.estados) or\
                len(afd1.estados_finais) != len(afd2.estados_finais) or\
                len(afd1.simbolos) != len(afd2.simbolos):
            return False

        palavras = AFD.combinacoes(afd1.simbolos, len(afd1.estados)-1)
        for palavra in palavras:
            if afd1.aceita(palavra) != afd2.aceita(palavra):
                return False
        return True
