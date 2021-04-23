from itertools import count
from re import sub
import pprint

pag1 = 'To do is to be to be is to do'
pag2 = 'To be or not to be I am what I am'
pag3 = 'I think therefore I am Do be do be do'
pag4 = 'Do do do da da da Let it be let it be'

class documento:


    def __init__(self, content = [str]):
        # OBS: caso modificar tratamento, modificar também 
        # na função processar do indiceInvertido

        tratamento = sub('[,.-;:!]', ' ', ' '.join(content).lower())
        self.conteudo = list(filter(lambda x: len(x)>0, tratamento.split(' ')))
        self.score = 0

        # print('Documento criado com conteúdo:', self.conteudo)


    def at_a_time(self, consulta = [str]):
        s = 0
        
        for c in consulta:
            s += self.conteudo.count(c.lower().strip())

        # print('Busca por termos: ', ', '.join(consulta),' = ', s, sep='')

        self.score = s
        return s


class indiceInvertido:


    def __init__(self, pags):
        self.vocabulario = dict()
        self.aparicoes = []
        self.paginas = pags
        return

    def compactarPostings(self):
        
        for svv in self.vocabulario.keys():
            j = [x[0] for x in self.vocabulario[svv]]
            # print(j)
            # faz a procedimento pra compactar e salvar o resultado
            l = j[:1]+list(map(lambda x: x-j[j.index(x)-1], j[1:]))
            
            for v in range(len(self.vocabulario[svv])):
                self.vocabulario[svv][v][0] = l[v]

    def contarVocabulos(self, pagina, vocabulo, aparicoes):
        
        if vocabulo not in self.vocabulario:
            self.vocabulario.update({vocabulo: []})
            self.vocabulario[vocabulo].append([pagina, aparicoes])
        
        else:
            self.vocabulario[vocabulo].append([pagina, aparicoes])

    def processar(self):
        c = 1
        
        for f in self.paginas:
            # f2 = f.lower().split(' ') # antigo: sem tratamento de string
            f2 = list(filter(lambda x: len(x)>0, sub('[,.-;:!]', ' ', f.lower()).split(' ')))
            
            for palavra in set(f2):
                conta = f2.count(palavra)
                self.contarVocabulos(pagina=c, vocabulo=palavra, aparicoes=conta)
            
            c += 1

        self.aparicoes = [(v, len(self.vocabulario[v])) for v in self.vocabulario.keys()]

def testar():
    # Testando indice invertido
    pp = pprint.PrettyPrinter(indent=4)

    def indice():
        ii = indiceInvertido([pag1, pag2, pag3, pag4])
        ii.processar()

        pp.pprint(ii.aparicoes)
        pp.pprint(ii.vocabulario)
        
        pp.pprint('Com compactação de postings')
        ii.compactarPostings()
        pp.pprint(ii.vocabulario)

    def d_time():
        d = documento(content = [pag1, pag2, pag3, pag4])
        pp.pprint(d.conteudo)
        pp.pprint(d.at_a_time(consulta = ['therefore', 'Let'])) # 3

    # indice()
    d_time()

# testar()
