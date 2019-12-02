

class GR:

    def __init__(self, nome=None, variaveis=[], terminais=[], producoes={}, variavel_inicial=None):
        self.nome = nome
        self.variaveis = variaveis
        self.terminais = terminais
        self.producoes = producoes
        self.variavel_inicial = variavel_inicial

    def __str__(self):
        output = f'\nnome={self.nome}'
        output += f'\nvariaveis={self.variaveis}'
        output += f'\nterminais={self.terminais}'
        output += f'\nvariavel_inicial={self.variavel_inicial}'
        output += f'\nproducoes='
        output += str([str(fp) + ' -> ' + str(e) for fp,
                       e in self.producoes.items()])
        return output

    def gera_arquivo(self, caminho_arquivo=None):
        if not caminho_arquivo:
            caminho_arquivo = self.nome + ".txt"

        with open(caminho_arquivo, 'w') as arquivo:
            arquivo.write(self.formato_saida())

    def formato_saida(self):
        output = self.nome + '=('
        output += '{' + ",".join(self.variaveis) + '},'
        output += '{' + ",".join(self.terminais) + '},'
        output += self.variavel_inicial + ','
        output += 'P)'
        output += '\nP\n'
        for v, producoes in self.producoes.items():
            for p in producoes:
                output += v + " -> " + p + '\n'
        return output
