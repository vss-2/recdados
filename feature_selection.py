from bs4 import BeautifulSoup
from csv import reader
from getRecDados import getPalavrasRem, getSitesLista
from unicodedata import normalize
from random import shuffle
import zipfile

def minerador(sopa, feats):
    # Implementação do TF-IDF
    tags_rm = getTagsRem()
    
    for t in tags_rm:
        for element in sopa.findAll(t):
            element.extract()

    dados = []
    bingo = [0]*len(feats)
    score_titulo = 0
    score_body = 0
    titulo = ''

    # Tentar pegar informação do título
    try:
        if sopa.title.string != None:
            titulo = sopa.title.string
            if('.' in titulo):
                titulo = titulo.replace('.', ' ')
            if('-' in titulo):
                titulo = titulo.replace('-', ' ')
            if(',' in titulo):
                titulo = titulo.replace(',', ' ')
            if('|' in titulo):
                titulo = titulo.replace('|', ' ')
            if(':' in titulo):
                titulo = titulo.replace(':', ' ')
            if('+' in titulo):
                titulo = titulo.replace('+', ' ')
            
            titulo = titulo.casefold().split(' ')

            for p in getPalavrasRem():
                if p in titulo:
                    titulo.remove(p)

            titulo = [t.strip() for t in titulo]

            for index, f in enumerate(feats, 0):
                if f in titulo:
                    b = titulo.count(f)
                    if index > len(feats)//2:
                        score_titulo -= b
                        bingo[index] = 1
                    else:
                        score_titulo += b
                        bingo[index] = 1
            
    except Exception as e:
        # print('Houve um problema no minerador() durante a avaliacao do score do titulo')
        pass

    # Tentar pegar informação de qualquer outro campo textual
    try:
        tags_sopa = sopa.findAll(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'span', 'p'])
        for ts in tags_sopa:
            try:
                dados.append(ts.getText().casefold().strip())
            except Exception as e:
                # print('Houve um problema no minerador() durante a insercao de palavras do body')
                pass
    except Exception as e:
        # print('Houve um problema no minerador() durante a coleta de campos textuais vindo das tags')
        pass

    try:
        titulo = list(filter(lambda x: x not in getPalavrasRem(), titulo))
    except Exception as e:
        # print('Houve um problema no minerador() durante a remocao de palavras do titulo')
        pass
    
    dados = list(filter(lambda x: x not in getPalavrasRem(), dados))

    for index, f in enumerate(feats, 0):
        if f in dados:
            if index > len(feats)//2:
                score_body -= dados.count(f)
            else:
                score_body += dados.count(f)

    bingo[-2] = score_titulo
    bingo[-1] = score_body

    return bingo

def featureSelection(posneg: str = 'pos', contar: bool = False):

    sites = getSitesLista()

    if posneg == 'pos':
        nstart, nend = 1,11
    else:
        nstart, nend = 11,21

    dados = []
    for s in sites:
        for n in range(nstart, nend):
            try:
                sopa = BeautifulSoup(open('./minerados/db/{}/{}.html'.format(s, n)).read(), features='html.parser')
            except FileNotFoundError:
                try: 
                    with zipfile.ZipFile('./10_sites_de_cada_exemplo.zip', 'r') as arqzip:
                        arqzip.extractall('./minerados/db/')
                except:    
                    print('Erro no featureSelection()\nPasta \'minerados/db/\' faltando, favor deszipar o arquivo \'10_sites_de_cada_exemplo.zip\' dentro dela')
                    exit()
            
            try:
                if sopa.title.string != None:
                    titulo = sopa.title.string

                    if('.' in titulo):
                        titulo = titulo.replace('.', ' ')
                    if('-' in titulo):
                        titulo = titulo.replace('-', ' ')
                    if(',' in titulo):
                        titulo = titulo.replace(',', ' ')
                    if('|' in titulo):
                        titulo = titulo.replace('|', ' ')
                    if(':' in titulo):
                        titulo = titulo.replace(':', ' ')
                    if('+' in titulo):
                        titulo = titulo.replace('+', ' ')
                    if('=' in titulo):
                        titulo = titulo.replace('=', ' ')
                    
                    titulo = titulo.casefold().split(' ')

                    for p in getPalavrasRem():
                        if p in titulo:
                            titulo.remove(p)

                    titulo = [t.strip() for t in titulo]
                    
                    dados.extend(titulo)
            except:
                # print('Houve um problema com a featureSelection() do titulo')
                pass
    
    s = set()
    gPR = getPalavrasRem()
    for d in dados:
        if not d in gPR:
            s.add(d)

    with open('feature_selection.csv', 'w') as arqcsv:
        for valor in dados:
            try:
                if valor in s and valor not in gPR:
                    if contar:
                        arqcsv.write(str(valor)+': '+str(dados.count(valor))+'\n')
                    else:
                        arqcsv.write(str(valor)+'\n')
                    s.remove(valor)
            except:
                # print('Houve um problema na featureSelection() dos valores')
                pass

    return 

def featureSelecionadas(n: int = 10, contar: bool = False) -> list:
    with open('feature_selection.csv', 'r') as arqcsv:
        leitor = reader(arqcsv, delimiter='\n')
        if contar:
            topfeats = [(l[0].split(': ')[0], int(l[0].split(': ')[1])) for l in leitor]
            topfeats.sort(key=lambda x: x[1], reverse=True)
            return topfeats[:n]
        else:
            topfeats = [l[0].split(': ')[0] for l in leitor]
            shuffle(topfeats)
        # print(topfeats)
        # print(topfeats[-n:])
    return topfeats[:n]

def selecionar(numfeats: int = 9):
    with open('features.csv', 'w') as arqcsv:
        print('Selecionando features')
        repetido = []

        featureSelection('pos', True)
        f = featureSelecionadas(numfeats*2, True)
        # print(f)
        for x in f:
            repetido.append(x[0])
            arqcsv.write(str(x[0])+',')
            if len(repetido)>numfeats:
                break

        featureSelection('neg', True)
        f = featureSelecionadas(numfeats*2, True)
        # print(f)
        f = [v[0] for v in f]
        for r in repetido:
            if r in f:
                f.remove(r)

        for x in f:
            if f.index(x) < numfeats:
                arqcsv.write(str(x)+',')
            else:
                arqcsv.write(str(x))
                break

# selecionar()
