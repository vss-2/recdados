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
import numpy as np
import pickle

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

def classificador(novos_dados: bool = False):
    if novos_dados or not exists('./features.csv'):
        novos_dados = True
        selecionar()
        # selecionar = Seleciona e gera o arquivo features.csv

    feats = None

    with open('features.csv', 'r') as arqcsv:
        feats = reader(arqcsv, delimiter=',')
        feats = [c for c in feats][0]
        m = []
        treino = pd.DataFrame()
        mil = dict()
        
        # Renomear todos os cantos onde está ricardoeletro
        
        if novos_dados:
            # Lê os treinos da loja específica
            
            for a in range(1, 21):
                if exists('./minerados/db/ricardoeletro/{}.html'.format(a)):
                    with open('./minerados/db/ricardoeletro/{}.html'.format(a), 'r') as arqhtml:
                        sopa = BeautifulSoup(arqhtml, 'html.parser')
                        m.append(minerador(sopa, feats))
            
            treino = pd.DataFrame(data = m, columns = feats)

            with open('./minerados/mil/ricardoeletro/treino', 'wb') as arqdados:
                pickle.dump(treino, arqdados)

            with open('./minerados/mil/ricardoeletro/m', 'wb') as arqdados:
                pickle.dump(m, arqdados)

        else:
            
            if exists('./minerados/mil/ricardoeletro/treino'):
                with open('./minerados/mil/ricardoeletro/treino', 'rb') as arqdados:
                    treino = pickle.load(arqdados)

            if exists('./minerados/mil/ricardoeletro/m'):
                with open('./minerados/mil/ricardoeletro/m', 'rb') as arqdados:
                    m = pickle.load(arqdados)

            else:
                print('Arquivo treino ou m não encontrado, tente rodar com o parâmetro novos_dados = True')
                exit()

        if novos_dados:
            
            # Lê os 1000 htmls da loja específica
            for a in range(1, 1000):
                if exists('./minerados/mil/ricardoeletro/{}.html'.format(a)):
                    with open('./minerados/mil/ricardoeletro/{}.html'.format(a), 'r') as arqhtml2:
                        sopa = BeautifulSoup(arqhtml2, 'html.parser')
                        k = minerador(sopa, feats)
                        mil.update({len(mil)+len(m):k})

            with open('./minerados/mil/ricardoeletro/mil', 'wb') as arqdados:
                pickle.dump(mil, arqdados)

        else:
            if exists('./minerados/mil/ricardoeletro/mil'):
                with open('./minerados/mil/ricardoeletro/mil', 'rb') as arqdados:
                    mil = pickle.load(arqdados)
            else:
                print('Arquivo mil não encontrado, tente rodar com o parâmetro novos_dados = True')
                exit()

        df = None

        # classificadores = ['Naive Bayes', 'Decision Tree', 'Multi Layer Perceptron', 'SVC', 'Regressao Logistica']
        # classificadores['Naive Bayes']
        df = pd.DataFrame(list(mil.values()), columns = feats)
        
        # for c in classificadores:
        #     if not exists('./minerados/mil/ricardoeletro/{}'.format(c)):
        #         with open('./minerados/mil/ricardoeletro/{}'.format(c), 'wb') as arqdados:
        #             pickle.dump(df, arqdados)
        #     else:
        #         with open('./minerados/mil/ricardoeletro/{}'.format(c), 'rb') as arqdados:
        #             df = arqdados.load(arqdados)
                    
        # Juntar dataframes treino e df caso seja necessário:
        # print(treino.append(df,ignore_index=True))

        gnb = GaussianNB()
        gnb.fit(treino, [1]*10+[0]*10)
        # print(df.head())
        result = gnb.predict(X=df)
        print(result)

classificador(novos_dados=False)
