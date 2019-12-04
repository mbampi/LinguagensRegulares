
import re
from AFD import AFD


class AFN:

    def __init__(self, nome=None, estados=[], simbolos=[], estado_inicial=None, estados_finais=[], funcoes_programa={}):
        self.nome = nome
        self.estados = estados
        self.simbolos = simbolos
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais
        self.funcoes_programa = funcoes_programa

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

    @staticmethod
    def afn_de_arquivo(caminho_arquivo):
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

                if funcoes_programa.get((estado, simbolo)):
                    funcoes_programa[(estado, simbolo)].append(
                        estado_resultante)
                else:
                    funcoes_programa[(estado, simbolo)] = [estado_resultante]

            return AFN(nome, estados, simbolos, estado_inicial, estados_finais, funcoes_programa)

    @staticmethod
    def _saidas_novo_estado(estado, simbolo, funcoes_programa):
        estados = estado.split('+')
        saidas = []
        for e in estados:
            estado_resultante = funcoes_programa.get((e, simbolo))
            if estado_resultante:
                saidas.extend(estado_resultante)
        if saidas == []:
            return 'QM'
        return '+'.join(sorted(list(set(saidas))))

    @staticmethod
    def _define_estados_finais(estados, estados_finais):
        finais = []
        for estado in estados:
            for ef in estados_finais:
                if ef in estado:
                    finais.append(estado)
        return finais

    def para_AFD(self):
        q = []
        t = {}
        q.append(self.estado_inicial)

        estado_morto = 'QM'

        for simbolo in self.simbolos:
            estado_resultante = self.funcoes_programa.get(
                (self.estado_inicial, simbolo))
            if estado_resultante:
                t[(self.estado_inicial, simbolo)] = '+'.join(estado_resultante)
            else:
                t[(self.estado_inicial, simbolo)] = estado_morto

        while(set(q) != set(t.values())):
            for er in list(t.values()):
                if er not in q:
                    q.append(er)
                    for simbolo in self.simbolos:
                        if '+' in er:
                            t[(er, simbolo)] = AFN._saidas_novo_estado(
                                er, simbolo, self.funcoes_programa)
                        else:
                            estado_resultante = self.funcoes_programa.get(
                                (er, simbolo))
                            if estado_resultante:
                                t[(er, simbolo)] = '+'.join(estado_resultante)
                            else:
                                t[(er, simbolo)] = estado_morto

        estados_finais = AFN._define_estados_finais(q, self.estados_finais)

        return AFD(nome=self.nome, estados=q, simbolos=self.simbolos, estado_inicial=self.estado_inicial, estados_finais=estados_finais, funcoes_programa=t)
