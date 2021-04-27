from itertools import count
from sklearn.metrics.pairwise import cosine_similarity
from numpy import array
from re import sub
from csv import reader
from os import listdir
from numpy import digitize
from math import log
from numpy import dot
from numpy.linalg import norm
from numpy import isnan
from numpy import bool8
from sys import getsizeof
import pprint
import pandas as pd
import re

pag1 = 'To do is to be to be is to do'
pag2 = 'To be or not to be I am what I am'
pag3 = 'I think therefore I am Do be do be do'
pag4 = 'Do do do da da da Let it be let it be'

class documento:


    def __init__(self, content = [str]):
        # OBS: caso modificar tratamento, modificar também 
        # na função processar do indiceInvertido
        tratamento = ' '.join(content).lower()
        tratamento = sub('[,.-;:!\'\n()]', ' ', tratamento)
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


    def __init__(self, pags, pols):
        self.vocabulario = dict()
        self.aparicoes = []
        self.paginas = pags
        self.polegadas = pols
        self.termos = []
        for p in self.paginas:
            # print(p)
            self.termos.append(len(p.lower().strip().split(' ')))
        # print(self.termos)
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
            f2 = list(filter(lambda x: len(x)>0, sub('[,.-;:!\'\n()]', ' ', f.lower()).split(' ')))
            
            for palavra in set(f2):
                conta = f2.count(palavra)
                self.contarVocabulos(pagina=c, vocabulo=palavra, aparicoes=conta)
            
            c += 1

        self.aparicoes = [(v, len(self.vocabulario[v])) for v in self.vocabulario.keys()]


def zoneScoring(document, queue = [str], g = dict):
    # OBS: Mudar a queue conforme campo muda, ex queue[0] é title queue[1] é o body

    # print(queue, (document.at_a_time(consulta = queue) > 0))
    return g['title'] * (document.at_a_time(consulta = queue) > 0) + g['body'] * (document.at_a_time(consulta = queue) > 0)


def cosScore(queue = [str], K = int, index = [indiceInvertido]):
    scores = [0] * len(index[0].termos)
    length = index[0].termos
    # print(index[0].vocabulario)
    
    for q in queue:
        # Tratar termo
        # Calcular importância do termo na query
        wtq = queue.count(q)/len(queue)

        # Buscar a posting list de cada documento
        busca = index[0].vocabulario[q]
        for b in busca:
            # 'ultrawide': [[218, 1], [226, 1]]
            scores[b[0]] += b[1] * wtq

        for s in range(len(scores)):
            scores[s] = scores[s]/length[s]

        # print(scores)

    for s in range(len(scores)):
        title = index[0].paginas[s].find('.html') + 5
        title = index[0].paginas[s][title:]
        scores[s] = (scores[s], s, title.strip())
        # scores[s] = (scores[s], s, index[0].paginas[s])

    scores.sort(key= lambda x: x[0], reverse=True)
    # for arq in scores[:K]:
        # print(arq[0])
        # print('->>>', index[0].paginas[arq[1]-1], '<<<-')

    return scores[:K]

def cosseno_limpo(queue = [str], K = int, infos = [indiceInvertido], field = dict):
    scores = [0] * (len(infos[0].termos)+1)
    scores2 = []
    for r in range(len(infos[0].termos)+1):
        scores2.append([0]*len(queue))
    length = infos[0].termos
    # print(infos[0].vocabulario)
    
    peso_query = []

    for q in queue:
        # Tratar termo
        # Calcular importância do termo na query
        wtq = queue.count(q)/len(queue)

        # Buscar a posting list de cada documento
        try:
            busca = field[q]
        except:
            # return None, None
            pass
        # print(busca)
        peso_query.append( (1+log(queue.count(q))) * log(len(infos[0].paginas)/len(busca)))
        for b in busca:
            # print(b)
            # 'ultrawide': [[218, 1], [226, 1]]
            # print(scores[b[0]])
            scores[b[0]] += b[1] * wtq
            # print(b[1] * log(len(infos[0].paginas)/b[1], 2) * wtq)
            scores2[b[0]][queue.index(q)] = ( b[1] * wtq ) / length[b[0]-1]

        # print(scores2)

        for s in range(len(scores)-1):
            scores[s] = scores[s]/length[s]

        # print(scores)

    for s in range(len(scores)-1):
        title = infos[0].paginas[s].find('.html') + 5
        title = infos[0].paginas[s][title:]
        scores[s] = (scores[s], s, title.strip())
        # scores[s] = (scores[s], s, infos[0].paginas[s])

    # scores.sort(key= lambda x: x[0], reverse=True)
    # for arq in scores[:K]:
        # print(arq[0])
        # print('<<<-', infos[0].paginas[arq[1]-1], '->>>')
    # print(scores2)

    return scores2, peso_query

def cosseno_tfidf(queue = [str], K = int, infos = [indiceInvertido], field = dict):
    scores = [0] * (len(infos[0].termos)+1)
    scores2 = []
    for r in range(len(infos[0].termos)+1):
        scores2.append([0]*len(queue))
    length = infos[0].termos
    # print(infos[0].vocabulario)
    
    peso_query = []

    for q in queue:
        # Tratar termo
        # Calcular importância do termo na query
        wtq = queue.count(q)/len(queue)

        # Buscar a posting list de cada documento
        try: 
            busca = field[q]
        except:
            # return None, None
            pass
        # print(busca)
        peso_query.append( (1+log(queue.count(q))) * log(len(infos[0].paginas)/len(busca)))
        for b in busca:
            # print(b)
            # 'ultrawide': [[218, 1], [226, 1]]
            # print(scores[b[0]])
            scores[b[0]] += b[1] * log(len(infos[0].paginas)/b[1], 2) * wtq
            # print(b[1] * log(len(infos[0].paginas)/b[1], 2) * wtq)
            scores2[b[0]][queue.index(q)] = ((1+ log(b[1], 2) * log(len(infos[0].paginas)/len(b), 2) * wtq))/length[b[0]-1]

        # print(scores2)

        for s in range(len(scores)-1):
            scores[s] = scores[s]/length[s]

        # print(scores)

    for s in range(len(scores)-1):
        title = infos[0].paginas[s].find('.html') + 5
        title = infos[0].paginas[s][title:]
        scores[s] = (scores[s], s, title.strip())
        # scores[s] = (scores[s], s, infos[0].paginas[s])

    # scores.sort(key= lambda x: x[0], reverse=True)
    # for arq in scores[:K]:
        # print(arq[0])
        # print('<<<-', infos[0].paginas[arq[1]-1], '->>>')
    # print(scores2)

    return scores2, peso_query


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

def main():
    pags = []
    discretizar = []
    marca = []
    tipo_tela = []
    
    df = pd.read_csv('./extraído/amazon - amazon.csv')

    # for arq in listdir('./extraído'):
    with open('./extraído/amazon - amazon.csv', 'r') as arqcsv:
        linhas = reader(arqcsv)
        for l in linhas:
            if l[1].lower().strip() != 'tamanho':
                posicao_marca = l[0].lower().strip().split(' ')
                if len(posicao_marca)>1:
                    l[0] = l[0].strip().lower().split(' ')[1]
                marca.append(l[0].lower().strip().replace('\'','').replace('\"','').replace(',','.'))
                discretizar.append(float(l[1].lower().strip().replace('\'','').replace('\"','').replace(',','.').replace(' polegadas','').replace(' centímetros','').replace(' pol','')))
                pags.append([k.strip()+' ' for k in l])
        pags.pop(0)
    
    pags = [''.join(x).lower() for x in pags]
    # print(df.dtypes)

    def tratar_marca(x):
        t = str(x).strip().lower().split(' ')
        if len(t)>1:
            t = t[1]
            return str(t).lower().strip().replace('\'','').replace('\"','').replace(',','.')
        return str(x).strip().lower()

    def tratar_tecnologia(x):
        t = str(x).strip().lower().split(' ')
        if len(t)>1:
            if '-' in t: t.remove('-')
            if 'crystal' in t: t.remove('crystal')
            if 'ultra' in t: t.remove('ultra')
            t = t[0]
            return str(t).lower().strip().replace('\'','').replace('\"','').replace(',','.').replace('\n','').replace('-','')
        return x.strip().lower()

    def tratar_tela(x):
        x = list(filter(lambda x: len(x)>1, sub('[,.-;:!\'\n()]x', ' ', x.lower().strip()).split(' ')))
        # print(x)
        if '8k' in x or '4320' in x: return '8k'
        if '3860' in x or '4k' in x: return '4k'
        if '2160' in x: return '2k'
        if '1080' in x or '19201080': return 'full hd'
        if '768' or '720' in x: return 'hd'
        return None


    df['Marca'] = df['Marca'].map(lambda x: tratar_marca(x))
    # print(df.Marca.values)
    df['Polegadas Discretas'] = digitize(discretizar, [25,50,75,100])
    # print(df['Polegadas Discretas'].values)
    df['Tamanho'] = discretizar
    # print(df.Tamanho.values)
    df['Tecnologia'] = df['Tecnologia'].map(lambda x: tratar_tecnologia(x))
    # print(df.Tecnologia.values)
    df['Tela'] = df['Tela'].map(lambda x: tratar_tela(x))
    # print(df.Tela.values)

    # print(df.Tela.unique())
    # print(pags[1])
    # print()
    # print(marca)
    ii = indiceInvertido(pags = pags, pols = discretizar)
    ii.processar()
    print(ii.vocabulario)
    ii.compactarPostings()
    print(ii.vocabulario)

    def espaco_vetor(indice, busca, df):
        resultado_semelhanca = []

        if type(busca) == str:
            b = list(filter(lambda x: len(x)>1, sub('[,.-;:!\'\n()]', ' ', busca.lower()).split(' ')))
        else:
            for r in range(len(busca)):
                busca.extend(list(filter(lambda x: len(x)>1, sub('[,.-;:!\'\n()]', ' ', busca[r].lower()).split(' '))))
            b = busca

        t_doc, t_bus = [], []
        for documento in indice[0].paginas:
            d = []
            if type(documento) == str:
                d = list(filter(lambda x: len(x)>1, sub('[,.-;:!\'\n()]', ' ', documento.lower()).split(' ')))
            else:
                for r in range(len(documento)):
                    d.extend(list(filter(lambda x: len(x)>1, sub('[,.-;:!\'\n()]', ' ', documento[r].lower()).split(' '))))

            # break
            sd = set(d)
            sb = set(b)
            # ambos serão uma lista, salvei conjunto só pra uso futuro (mais rápido)

            # token de feito a partir de todos os documentos
            
            # print(list(tokens))
            tokens = map(lambda x: x[0], indice[0].aparicoes)
            temp_doc, temp_bus = [], []

            for t in tokens:
                if t in d: temp_doc.append(1)
                else: temp_doc.append(0)
                if t in b: temp_bus.append(1)
                else: temp_bus.append(0)
            
            t_doc.extend([temp_doc])
            t_bus.extend([temp_bus])
            
            resultado_semelhanca.append((dot(temp_doc, temp_bus) / (norm(temp_doc) * norm(temp_bus))))
            # print('Resultado da semelhança espaco vetorial:', resultado_semelhanca[-1:])

        df['Resultado Cosseno'] = ['Resultado Cosseno'] + resultado_semelhanca
        return t_doc, t_bus

    # r1, r2 = espaco_vetor([ii], busca=['samsung', 'led'], df=df)
    # print(df['Resultado Cosseno'])

    def correlacao_spearman(r1, r2):
        quadrado = []
        ranking1 = r1
        ranking2 = r2
        
        for i in range(len(ranking1)):
            for j in range(len(ranking2)):
                if ranking1[i] == ranking2[j]:
                    quad = (i-j)**2
                else:
                    quad = 0
                quadrado.append(quad)
        
        d = ranking1 + ranking2
        return 1 - ( (6*sum(quadrado)) / (len(d) * ( (len(d)**2)-1) ) )

    resultados_spearman = []
    # print(r1)

    # for r in range(len(r1)):
    #     resultados_spearman.append(correlacao_spearman(r1[r], r2[r]))
    # print(resultados_spearman[:10])

    pp = pprint.PrettyPrinter(indent=4)

    # print(df.Marca.str.contains('samsung', regex=False))

    # def field_index_idf(termo, campo):
    #     idf = []
    #     for x in range(len(df[campo])):
    #         times = df[campo][x].count(termo)
    #         if times > 0:
    #             idf.append((x, times))
    #     return idf

    # print(field_index_idf('lg', 'Marca'))

    # ---------------- Criando Field Index ---------------------
    field_index = dict({'Marca': dict(), 'Tecnologia': dict(), 'Tela': dict()})
    for m in df.Marca.unique():
        m_array = field_index_idf(m, 'Marca')
        field_index['Marca'].update(dict({m: m_array}))

    # pp.pprint(field_index['Marca'])

    for m in df.Tecnologia.unique():
        m_array = field_index_idf(m, 'Tecnologia')
        field_index['Tecnologia'].update(dict({m: m_array}))

    # pp.pprint(field_index['Tecnologia'])

    for m in df.Tela.unique():
        m_array = field_index_idf(m, 'Tela')
        field_index['Tela'].update(dict({m: m_array}))

    # pp.pprint(field_index['Tela'])
    
    # print(field_index)
    # pp.pprint(field_index)
    # ----------------------------------------------------------

    # field_index = pd.DataFrame()
    
    # print(df['Marca'].unique())
    # print(df['Tamanho'].unique())
    # print(df['Tecnologia'].unique())
    # print(df['Tela'].unique())
    # print(df['Entradas'].unique())

    # pp.pprint(pags[1])
    # pp.pprint(sorted(ii.vocabulario))
    # pp.pprint(ii.vocabulario)
    # pp.pprint(ii.aparicoes)
    # print(ii.vocabulario)
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
            # if z != 0.0:
                # print('Zone Scoring de ', b, ': ', z, sep='')

    # cs = cosScore(queue = ['tcl'], K = 10, index = [ii])
    # dn, q = 
    dn, q = cosseno_tfidf(queue = ['tcl', 'samsung'], K = 10, index = [ii])
    
    sim = []

    c = 0
    for n in dn:
        if n == [0,0]: sim.append((0, c))
        else: 
            # print(n, q)
            sim.append(( (dot(n, q) / ( norm(n) * norm(q) )), c))
        c+=1
    
    sim.sort(key=lambda x: x[0], reverse=True)
    # print([x[1] for x in sim_limpo])
    # print('Cosseno TF-IDF', [x[1] for x in sim])

    # -------------------------------------------------------------------------
    
    dn_limpo, q_limpo = cosseno_limpo(queue = ['tcl', 'lcd'], K = 10, index = [ii])
    
    sim_limpo = []

    c = 0
    for n in dn_limpo:
        if n == [0,0]: sim_limpo.append((0, c))
        else: 
            # print(n, q)
            sim_limpo.append(( (dot(n, q_limpo) / ( norm(n) * norm(q_limpo) )), c))
        c+=1

    sim_limpo.sort(key=lambda x: x[0], reverse=True)
    # print('Cosseno com TF', [x[1] for x in sim_limpo])

    print(correlacao_spearman(sim, sim_limpo))
    print(field_index['Tela'].keys())

    # pp.pprint(cs)

# main()

df = pd.read_csv('./extraído/amazon - amazon.csv')
pags = []
discretizar = []
marca = []
tipo_tela = []

def tratar_marca(x):
    t = str(x).strip().lower().split(' ')
    if len(t)>1:
        t = t[1]
        return str(t).lower().strip().replace('\'','').replace('\"','').replace(',','.')
    return str(x).strip().lower()

def tratar_tecnologia(x):
    t = str(x).strip().lower().split(' ')
    if len(t)>1:
        if '-' in t: t.remove('-')
        if 'crystal' in t: t.remove('crystal')
        if 'ultra' in t: t.remove('ultra')
        t = t[0]
        return str(t).lower().strip().replace('\'','').replace('\"','').replace(',','.').replace('\n','').replace('-','')
    return x.strip().lower()

def tratar_tela(x):
    x = list(filter(lambda x: len(x)>1, sub('[,.-;:!\'\n()]x', ' ', x.lower().strip()).split(' ')))
    # print(x)
    if '8k' in x or '4320' in x: return '8k'
    if '3860' in x or '4k' in x: return '4k'
    if '2160' in x: return '2k'
    if '1080' in x or '19201080': return 'full hd'
    if '768' or '720' in x: return 'hd'
    return None

with open('./extraído/amazon - amazon.csv', 'r') as arqcsv:
    linhas = reader(arqcsv)
    for l in linhas:
        if l[1].lower().strip() != 'tamanho':
            posicao_marca = l[0].lower().strip().split(' ')
            if len(posicao_marca)>1:
                l[0] = l[0].strip().lower().split(' ')[1]
            marca.append(l[0].lower().strip().replace('\'','').replace('\"','').replace(',','.'))
            discretizar.append(float(l[1].lower().strip().replace('\'','').replace('\"','').replace(',','.').replace(' polegadas','').replace(' centímetros','').replace(' pol','')))
            pags.append([k.strip()+' ' for k in l])
    pags.pop(0)

df['Marca'] = df['Marca'].map(lambda x: tratar_marca(x))
# print(df.Marca.values)
df['Polegadas Discretas'] = digitize(discretizar, [25,50,75,100])
# print(df['Polegadas Discretas'].values)
df['Tamanho'] = discretizar
# print(df.Tamanho.values)
df['Tecnologia'] = df['Tecnologia'].map(lambda x: tratar_tecnologia(x))
# print(df.Tecnologia.values)
df['Tela'] = df['Tela'].map(lambda x: tratar_tela(x))
# print(df.Tela.values)

def gama_compactacao(valor):
    log2 = lambda x: log(x, 2)
    
    def unario(x):
        return (x-1)*'0'+'1'
    
    def binario(x, l = 1):
        s = '{0:0%db}' % l
        return s.format(x)
        
    def gama(x):
        if(x == 0): 
            return '0'
    
        n = 1 + int(log2(x))
        b = x - 2**(int(log2(x)))
    
        l = int(log2(x))
    
        k = unario(n) + binario(b, l)
        return array([int(x) for x in k])
    
    return gama(valor)
    # print(gama(10))

compactar_field = True
compactar_gama  = True
compactados = [0, 0, 0]
pp = pprint.PrettyPrinter(indent=4)

def comparar_compactacao(p1, p2, p3):
    compactados[0] += getsizeof(p1)
    compactados[1] += getsizeof(p2)
    compactados[2] += getsizeof(p3)
    # print(compactados)
    return

def field_index_idf(termo, campo):
    idf = []
    for x in range(len(df[campo])):
        times = df[campo][x].count(termo)
        if times > 0:
            idf.append((x, times))
    # print(idf, '------------------------------------')

    idf2 = idf.copy()
    idf3 = idf.copy()

    if compactar_field:
        l = list(map(lambda x: x[0]-idf2[idf2.index(x)-1][0], idf2[1:]))
        for x in range(1, len(idf2)):
            if compactar_gama == True:
                idf3[x] = (gama_compactacao(l[x-1]), idf2[x][1])
            idf2[x] = (l[x-1], idf2[x][1])
        
    # print(idf2, idf3)
    comparar_compactacao(idf, idf2, idf3)
    print(termo, campo)
    # pp.pprint(idf)
    pp.pprint(idf2)
    # pp.pprint(idf3)
    return idf


field_index = dict({'Marca': dict(), 'Tecnologia': dict(), 'Tela': dict()})
for m in df.Marca.unique():
    m_array = field_index_idf(m, 'Marca')
    field_index['Marca'].update(dict({m: m_array}))

# pp.pprint(field_index['Marca'])

for m in df.Tecnologia.unique():
    m_array = field_index_idf(m, 'Tecnologia')
    field_index['Tecnologia'].update(dict({m: m_array}))

# pp.pprint(field_index['Tecnologia'])

for m in df.Tela.unique():
    m_array = field_index_idf(m, 'Tela')
    field_index['Tela'].update(dict({m: m_array}))

print('Tamanho do field index sem compactação:', compactados[0],
    '\nTamanho do field index com compactação:', compactados[1],
    '\nTamanho do field index com Gama Code:', compactados[2])


with open('./extraído/amazon - amazon.csv', 'r') as arqcsv:
    linhas = reader(arqcsv)
    for l in linhas:
        if l[1].lower().strip() != 'tamanho':
            posicao_marca = l[0].lower().strip().split(' ')
            if len(posicao_marca)>1:
                l[0] = l[0].strip().lower().split(' ')[1]
            marca.append(l[0].lower().strip().replace('\'','').replace('\"','').replace(',','.'))
            discretizar.append(float(l[1].lower().strip().replace('\'','').replace('\"','').replace(',','.').replace(' polegadas','').replace(' centímetros','').replace(' pol','')))
            pags.append([k.strip()+' ' for k in l])
    pags.pop(0)

pags = [''.join(x).lower() for x in pags]

# Criação de Postings (Vocabulário)
ii = indiceInvertido(pags = pags, pols = discretizar)

def correlacao_spearman(r1, r2):
    quadrado = []
    ranking1 = r1
    ranking2 = r2
    
    for i in range(len(ranking1)):
        for j in range(len(ranking2)):
            if ranking1[i] == ranking2[j]:
                quad = (i-j)**2
            else:
                quad = 0
            quadrado.append(quad)
    
    d = ranking1 + ranking2
    return 1 - ( (6*sum(quadrado)) / (len(d) * ( (len(d)**2)-1) ) )

def processamento_consulta(entrada):
    # (field_index) Marca.consulta
    campo = entrada[0]
    # if entrada['Marca'] != '':
    #     campo = entrada['Marca']  # 'Marca'
    # if entrada['Tecnologia'] != '':
    #     tecnologia = entrada['Tecnologia']
    # if entrada['Tela'] != '':
    #     tela = entrada['Tela']
    # if entrada['Polegada'] != '':
    #     polegada = entrada['Polegada']
    
    pesquisa = entrada[1] # ['Samsung', 'led']
    
    dn, q = cosseno_tfidf(queue = pesquisa, infos=[ii], field=field_index[campo])
    dn_limpo, q_limpo = cosseno_limpo(queue = pesquisa, infos=[ii], field=field_index[campo])

    sim = []
    c = 0
    for n in dn:
        if n == [0,0]: sim.append((0, c))
        else: 
            # print(n, q)
            sim.append(( (dot(n, q) / ( norm(n) * norm(q) )), c))
        c+=1
    sim = list(filter(lambda x: isnan(x[0]) == False, sim))
    sim.sort(key=lambda x: x[0], reverse=True)
    # print('Cosseno TF-IDF', [x[1] for x in sim])

    # -------------------------------------------------------------------------

    sim_limpo = []
    c = 0
    for n in dn_limpo:
        if n == [0,0]: sim_limpo.append((0, c))
        else: 
            # print(n, q)
            sim_limpo.append(( (dot(n, q_limpo) / ( norm(n) * norm(q_limpo) )), c))
        c+=1
    sim_limpo = list(filter(lambda x: isnan(x[0]) == False, sim_limpo))
    sim_limpo.sort(key=lambda x: x[0], reverse=True)
    # print('Cosseno com TF', [x[1] for x in sim_limpo])
    
    # print(sim[:40], sim_limpo[:40], sep='\n')
    # print(correlacao_spearman(sim, sim_limpo))
    busca1 = [str(x[1]) for x in sim[:]]
    title = []
    for x in busca1:
        title.append(df.title[int(x)])
    busca1 = list(zip(busca1, title))
    return correlacao_spearman(sim, sim_limpo), busca1, title

# processamento_consulta(['Marca', ['samsung']])

def comentarios():
    # sim = []
    # c = 0
    # for n in dn:
    #     if sum(n) == 0:
    #         continue
    #     k = dot(n, q) / ( norm(n) * norm(q))
    #     # print(type(k), k)
    #     if isnan(k): sim.append((0, c))
    #     else: sim.append((k, c))
    #     c+=1
    # sim.sort(key=lambda x: x[0], reverse=True)
    # # print('Cosseno TF-IDF', [x[1] for x in sim])
    # # -------------------------------------------------------------------------

    # sim_limpo = []
    # c = 0
    # for n in dn_limpo:
    #     if sum(n) == 0:
    #         continue
    #     k = dot(n, q) / ( norm(n) * norm(q))
    #     # print(type(k), k)
    #     if isnan(k): sim_limpo.append((0, c))
    #     else: sim_limpo.append((k, c))
    #     c+=1
    # sim_limpo.sort(key=lambda x: x[0], reverse=True)
    return none