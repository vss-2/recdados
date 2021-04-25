from itertools import count
from sklearn.metrics.pairwise import cosine_similarity
from numpy import array
from re import sub
from csv import reader
from os import listdir
import pprint

pag1 = 'To do is to be to be is to do'
pag2 = 'To be or not to be I am what I am'
pag3 = 'I think therefore I am Do be do be do'
pag4 = 'Do do do da da da Let it be let it be'

class documento:


    def __init__(self, content = [str]):
        # OBS: caso modificar tratamento, modificar também 
        # na função processar do indiceInvertido
        tratamento = ' '.join(content).lower()
        tratamento = sub('[,.-;:!]', ' ', tratamento)
        self.conteudo = list(filter(lambda x: len(x)>0, tratamento.split(' ')))
        self.score = 0

        # print('Documento criado com conteúdo:', self.conteudo)


    def at_a_time(self, consulta = [str]):
        s = 0

        if (len(consulta) == 1):
            consulta.append('')
        
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


def zoneScoring(document, queue = [str], g = dict):
    # OBS: Mudar a queue conforme campo muda, ex queue[0] é title queue[1] é o body

    # print(queue, (document.at_a_time(consulta = queue) > 0))
    return g['title'] * (document.at_a_time(consulta = queue) > 0) + g['body'] * (document.at_a_time(consulta = queue) > 0)

def cossenoScore(queue = [str], K = int, index = [indiceInvertido]):
    scores = []
    tamanho = [len(i.vocabulario) for i in index]
    queue = [q.lower().strip() for q in queue]
    for q in queue:
        if q in index[0].vocabulario.keys() and q in index[1].vocabulario.keys():
            print(index[0].vocabulario[q])
            scores.append(cosine_similarity(array(index[0].vocabulario[q]), array(index[1].vocabulario[q])))
        else:
            print('Palavra procurada:', q ,'não está no índice invertido, vou pular!')
            continue
    for d in range(len(scores)):
        scores[d] = scores[d][0]/tamanho[d]
    return scores[:K]

def cosScore(queue = [str], K = int, index = [indiceInvertido]):
    scores = []

    tamanho = [len(x.paginas) for x in index]
    tamanho_array = []

    for q in queue:
        wtq = queue.count(q)/len(queue)
        wftd = 0
        c = 0
        for i in index:
            total = 0

            for a in i.aparicoes:
                if a[0] == q:
                    wftd += a[1]
                total += a[1]
            tamanho_array.append(wftd/total)

            if wftd != 0:
                scores.append(wtq * wftd)
            else:
                print('Não encontrei:', q)
                scores.append(0)

            print(len(scores), len(tamanho))
            for d in range(tamanho[c] - 1):
                scores[d] = scores[d]/tamanho[d]
            
            c += 1
    
    print(scores)
    
    return scores[:K]


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

    def z_scoring():
        d = documento(content = [pag1, pag2, pag3, pag4])
        pesos = dict({'body': 0.6, 'title': 0.4})
        queue = ['therefore', 'Let']
        for q in queue:
            z = zoneScoring(document = d, queue = [q], g = pesos)
            print('Zone Scoring de ', q, ': ', z, sep='') # 1.0 1.0
        queue = ['Luciano', 'Let']
        for q in queue:
            z = zoneScoring(document = d, queue = [q], g = pesos)
            print('Zone Scoring de ', q, ': ', z, sep='') # 0.0 1.0

    def c_score():
        ii = indiceInvertido([pag1, pag2])
        ii2 = indiceInvertido([pag3, pag4])
        ii.processar()
        ii2.processar()
        # Ele identifica corretamente que to não faz parte de pag3 e pag4
        # Ele está calculando: Resultado do Cosseno Score: [array([0.11111111, 0.10540926])]
        print('Resultado do Cosseno Score:',
            cossenoScore(queue = ['be', 'to'], K = 2, index = [ii, ii2]))
    
    indice()
    d_time()
    z_scoring()
    c_score()
    

# testar()

pags = []

for arq in listdir('./extraído'):
    with open('./extraído/'+arq, 'r') as arqcsv:
        linhas = reader(arqcsv)
        for l in linhas:
            pags.append([k.strip() for k in l])
        pags.pop(0)

    pags = [' '.join(p) for p in pags]
    # print(pags[1])

ii = indiceInvertido(pags = pags)
ii.processar()

pp = pprint.PrettyPrinter(indent=4)
# print(ii.vocabulario)
# print(ii.aparicoes)
docs = []
for p in pags:
    docs.append(documento(content = p))
# print(d.at_a_time(['Samsung', 'LED']))

pesos = dict({'body': 0.6, 'title': 0.4})
busca = ['Samsung', 'Wi-fi']
for b in busca:
    b = b.lower().strip()
    for d in docs:
        z = zoneScoring(document = d, queue = [b], g = pesos)
        if z != 0.0:
            print('Zone Scoring de ', b, ': ', z, sep='')

cosScore(queue = ['philco', 'brilho'], K = 10, index = [ii])

