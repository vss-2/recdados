from numpy import reshape, array
from numpy.random import shuffle
from getRecDados import getRotulos, getTagsRem, getPalavrasRem
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from csv import reader
from os.path import exists
from feature_selection import selecionar
from bs4 import BeautifulSoup
import pandas as pd

def minerador(sopa, feats):
    tags_rm = getTagsRem()
    
    for t in tags_rm:
        for element in sopa.findAll(t):
            element.extract()

    dados = []
    bingo = [0]*len(feats)
    soma = 0

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
                        soma -= b
                        bingo[index] = 1
                    else:
                        soma += b
                        bingo[index] = 1
            
            # dados.extend(titulo)
    except Exception as e:
        print(e)
        pass

    # Tentar pegar informação de qualquer outro campo textual
    try:
        tags_sopa = sopa.findAll(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'span', 'p'])
        for ts in tags_sopa:
            try:
                dados.append(ts.getText().casefold().strip())
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        pass

    dados = list(filter(lambda x: x not in getPalavrasRem(), dados))

    for index, f in enumerate(feats, 0):
        if f in dados:
            if index > len(feats)//2:
                soma -= dados.count(f)
            else:
                soma += dados.count(f)

    # print(bingo, soma)

    return bingo

def main():
    # selecionar()
    feats = None
    with open('features.csv', 'r') as arqcsv:
        feats = reader(arqcsv, delimiter=',')
        feats = [c for c in feats][0]
        m = []
        
        for a in range(1, 21):
            if exists('./minerados/db/ricardoeletro/{}.html'.format(a)):
                with open('./minerados/db/ricardoeletro/{}.html'.format(a), 'r') as arqhtml:
                    sopa = BeautifulSoup(arqhtml, 'html.parser')
                    m.append(minerador(sopa, feats))
        
        # Coluna SIM/NAO identifica se é realmente um televisor
        for index, v in enumerate(m):
            if index>9:
                v.append(0)
            else:
                v.append(1)

        feats.append('SIM/NAO')
        df = pd.DataFrame(data=m, columns=feats)
        print(df.head(20))
        
        # mil = dict()
        # for a in range(1, 1000):
        #     if exists('./minerados/mil/ricardoeletro/{}.html'.format(a)):
        #         with open('./minerados/mil/ricardoeletro/{}.html'.format(a), 'r') as arqhtml2:
        #             sopa = BeautifulSoup(arqhtml2, 'html.parser')
        #             mil.update({len(mil)+len(m):minerador(sopa, feats)})
        
        # df += pd.DataFrame(mil)
        # print(df.head(50))

main()