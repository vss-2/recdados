from numpy import reshape, array
from numpy.random import shuffle
from getRecDados import getRotulos, getTagsRem, getPalavrasRem, getSitesLista
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
from sklearn.metrics import accuracy_score, f1_score
# import mlflow
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
    score_titulo = 0
    score_body = 0

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

    titulo = list(filter(lambda x: x not in getPalavrasRem(), titulo))
    dados = list(filter(lambda x: x not in getPalavrasRem(), dados))

    for index, f in enumerate(feats, 0):
        if f in dados:
            if index > len(feats)//2:
                score_body -= dados.count(f)
            else:
                score_body += dados.count(f)

    # print(bingo, soma)
    # print(titulo, dados)

    bingo[-2] = score_titulo
    bingo[-1] = score_body

    return bingo

def classificador(novos_dados: bool = False):
    numfeats = 9
    if novos_dados or not exists('./features.csv'):
        novos_dados = True
        selecionar(numfeats)
        # selecionar(numfeats) = Seleciona int(numfeats) e gera o arquivo features.csv

    feats = None

    # gSL = getSitesLista()
    gSL = ['ricardoeletro']

    with open('features.csv', 'r') as arqcsv:
        feats = reader(arqcsv, delimiter=',')
        feats = [c for c in feats][0]
        feats.append('Score Titulo')
        feats.append('Score Body')
        for site in gSL:
            m = []
            treino = pd.DataFrame()
            mil = dict()
            
            # Renomear todos os cantos onde está ricardoeletro
            
            if novos_dados:
                # Lê os treinos da loja específica
                
                for a in range(1, 21):
                    if exists('./minerados/db/{}/{}.html'.format(site, a)):
                        with open('./minerados/db/{}/{}.html'.format(site, a), 'r') as arqhtml:
                            sopa = BeautifulSoup(arqhtml, 'html.parser')
                            k = minerador(sopa, feats)
                            m.append(k)
                
                treino = pd.DataFrame(data = m, columns = feats)

                with open('./minerados/mil/{}/treino'.format(site), 'wb') as arqdados:
                    pickle.dump(treino, arqdados)

                with open('./minerados/mil/{}/m'.format(site), 'wb') as arqdados:
                    pickle.dump(m, arqdados)

            else:
                
                if exists('./minerados/mil/{}/treino'.format(site)):
                    with open('./minerados/mil/{}/treino'.format(site), 'rb') as arqdados:
                        treino = pickle.load(arqdados)

                if exists('./minerados/mil/{}/m'.format(site)):
                    with open('./minerados/mil/ricardoeletro/m', 'rb') as arqdados:
                        m = pickle.load(arqdados)

                else:
                    print('Arquivo treino ou m não encontrado, tente rodar com o parâmetro novos_dados = True')
                    exit()

            if novos_dados:
                
                # Lê os 1000 htmls da loja específica
                for a in range(1, 1000):
                    if exists('./minerados/mil/{}/{}.html'.format(site, a)):
                        with open('./minerados/mil/{}/{}.html'.format(site, a), 'r') as arqhtml2:
                            sopa = BeautifulSoup(arqhtml2, 'html.parser')
                            k = minerador(sopa, feats)
                            mil.update({len(mil)+len(m):k})

                with open('./minerados/mil/{}/mil'.format(site), 'wb') as arqdados:
                    pickle.dump(mil, arqdados)

            else:
                if exists('./minerados/mil/{}/mil'.format(site)):
                    with open('./minerados/mil/{}/mil'.format(site), 'rb') as arqdados:
                        mil = pickle.load(arqdados)
                else:
                    print('Arquivo mil não encontrado, tente rodar com o parâmetro novos_dados = True')
                    exit()

            df = pd.DataFrame(list(mil.values()), columns = feats)

            # Juntar dataframes treino e df caso seja necessário:
            # print(treino.append(df,ignore_index=True))

            # print(df.head())
            # gnb, dtc, mlp, svc, lgr = GaussianNB(), DecisionTreeClassifier(), MLPClassifier(), SVC(), LogisticRegression()

            gnb = GaussianNB()
            gnb.fit(treino, [1]*(numfeats+1) + [0]*(numfeats+1))
            result = gnb.predict(X=df)
            score = gnb.score(X=df, y = result)
            print('Resultado Naive Bayes: \n', result)

            # dtc.fit(treino, [1]*10+[0]*10)
            # result = dtc.predict(X=df)
            # score = dtc.score(X=df, y = result)
            # print('Resultado Decision Tree: \n', result)

            # mlp.fit(treino, [1]*10+[0]*10)
            # result = mlp.predict(X=df)
            # score = mlp.score(X=df, y = result)
            # print('Resultado Multi-layer Perceptron: \n', result)

            # svc.fit(treino, [1]*10+[0]*10)
            # result = svc.predict(X=df)
            # score = svc.score(X=df, y = result)
            # print('Resultado SVC: \n', result)

            # lgr.fit(treino, [1]*10+[0]*10)
            # result = lgr.predict(X=df)
            # score = lgr.score(X=df, y = result)
            # print('Resultado Logistic Regression: \n', result)

classificador(novos_dados=False)
