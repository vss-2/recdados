from numpy import reshape, array
from numpy.random import shuffle
from getRecDados import getRotulos, getTagsRem, getPalavrasRem, getSitesLista
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from csv import reader
from os.path import exists
from feature_selection import selecionar
from bs4 import BeautifulSoup
from sklearn.metrics import accuracy_score, f1_score
import mlflow
import pandas as pd
import numpy as np
import pickle

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

    try:
        titulo = list(filter(lambda x: x not in getPalavrasRem(), titulo))
    except Exception as e:
        # print(e)
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

def classificador(novos_dados: bool = False, heuristica: bool = False):
    numfeats = 9
    if novos_dados or not exists('./features.csv'):
        novos_dados = True
        selecionar(numfeats)
        # selecionar(numfeats) = Seleciona int(numfeats) e gera o arquivo features.csv

    feats = None

    if heuristica:
        pasta = 'heuristica'
    else:
        pasta = 'baseline'

    # gSL = getSitesLista()
    gSL = ['ricardoeletro','magazineluiza','colombo','havan','carrefour','amazon','mercadolivre']

    with open('features.csv', 'r') as arqcsv:
        feats = reader(arqcsv, delimiter=',')
        feats = [c for c in feats][0]
        feats.append('Score Titulo')
        feats.append('Score Body')
        for site in gSL:
            print(site)
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

                with open('./minerados/mil/{}/{}/treino'.format(pasta, site), 'wb') as arqdados:
                    pickle.dump(treino, arqdados)

                with open('./minerados/mil/{}/{}/m'.format(pasta, site), 'wb') as arqdados:
                    pickle.dump(m, arqdados)

            else:
                
                if exists('./minerados/mil/{}/{}/treino'.format(pasta, site)):
                    with open('./minerados/mil/{}/{}/treino'.format(pasta, site), 'rb') as arqdados:
                        treino = pickle.load(arqdados)

                if exists('./minerados/mil/{}/{}/m'.format(pasta, site)):
                    with open('./minerados/mil/{}/{}/m'.format(pasta, site), 'rb') as arqdados:
                        m = pickle.load(arqdados)

                else:
                    print('Arquivo treino ou m não encontrado, tente rodar com o parâmetro novos_dados = True')
                    exit()

            if novos_dados:
                    
                if exists('./minerados/mil/{}/{}/1010.html'.format(pasta, site)):
                    for a in range(1001, 2000):
                        if exists('./minerados/mil/{}/{}/{}.html'.format(pasta, site, a)):
                            with open('./minerados/mil/{}/{}/{}.html'.format(pasta, site, a), 'r') as arqhtml2:
                                sopa = BeautifulSoup(arqhtml2, 'html.parser')
                                k = minerador(sopa, feats)
                                mil.update({len(mil)+len(m):k})
                else:
                    # Lê os 1000 htmls da loja específica
                    for a in range(1, 1000):
                        if exists('./minerados/mil/{}/{}/{}.html'.format(pasta, site, a)):
                            with open('./minerados/mil/{}/{}/{}.html'.format(pasta, site, a), 'r') as arqhtml2:
                                sopa = BeautifulSoup(arqhtml2, 'html.parser')
                                k = minerador(sopa, feats)
                                mil.update({len(mil)+len(m):k})

                with open('./minerados/mil/{}/{}/mil'.format(pasta, site), 'wb') as arqdados:
                    pickle.dump(mil, arqdados)

            else:
                if exists('./minerados/mil/{}/{}/mil'.format(pasta, site)):
                    with open('./minerados/mil/{}/{}/mil'.format(pasta, site), 'rb') as arqdados:
                        mil = pickle.load(arqdados)
                else:
                    print('Arquivo mil não encontrado, tente rodar com o parâmetro novos_dados = True')
                    exit()

            df = pd.DataFrame(list(mil.values()), columns = feats)

            # Juntar dataframes treino e df caso seja necessário:
            # print(treino.append(df,ignore_index=True))
            # print(df.head())

            gnb, rfc, mlp, svc, lgr = GaussianNB(), RandomForestClassifier(), MLPClassifier(), SVC(), LogisticRegression()

            gnb = GaussianNB()
            gnb.fit(treino, [1]*(numfeats+1) + [0]*(numfeats+1))
            result = gnb.predict(X=df)
            score = gnb.score(X=df, y=result)
            with open('./minerados/mil/{}/{}/gnb'.format(pasta, site), 'wb') as arqdados:
                pickle.dump(result, arqdados)
            print('Resultado Naive Bayes: \n', result)

            rfc.fit(treino, [1]*(numfeats+1) + [0]*(numfeats+1))
            result = rfc.predict(X=df)
            score = rfc.score(X=df, y=result)
            with open('./minerados/mil/{}/{}/rfc'.format(pasta, site), 'wb') as arqdados:
                pickle.dump(result, arqdados)
            print('Resultado Random Forest Classifier: \n', result)

            mlp.fit(treino, [1]*(numfeats+1) + [0]*(numfeats+1))
            result = mlp.predict(X=df)
            score = mlp.score(X=df, y=result)
            with open('./minerados/mil/{}/{}/mlp'.format(pasta, site), 'wb') as arqdados:
                pickle.dump(result, arqdados)
            print('Resultado Multi-layer Perceptron: \n', result)

            svc.fit(treino, [1]*(numfeats+1) + [0]*(numfeats+1))
            result = svc.predict(X=df)
            score = svc.score(X=df, y=result)
            with open('./minerados/mil/{}/{}/svc'.format(pasta, site), 'wb') as arqdados:
                pickle.dump(result, arqdados)
            print('Resultado SVC: \n', result)

            lgr.fit(treino, [1]*(numfeats+1) + [0]*(numfeats+1))
            result = lgr.predict(X=df)
            score = lgr.score(X=df, y=result)
            with open('./minerados/mil/{}/{}/lgr'.format(pasta, site), 'wb') as arqdados:
                pickle.dump(result, arqdados)
            print('Resultado Logistic Regression: \n', result)

# classificador(novos_dados=True, heuristica=False)

def classificadorCompleto():
    gSL = ['ricardoeletro','magazineluiza','colombo','havan','carrefour','amazon','mercadolivre']
    resultadoCompleto = []
    pasta = 'baseline'
    for site in gSL:
        try:
            classificadores = ['gnb', 'rfc', 'mlp', 'svc', 'lgr']
            for c in classificadores:
                with open('./minerados/mil/{}/{}/{}'.format(pasta, site, c), 'rb') as arqdados:
                    l = pickle.load(arqdados)
                    resultadoCompleto.append(l)
        except Exception as e:
            continue
    # for rC in resultadoCompleto:
        # print(rC)

classificadorCompleto()

# https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html
# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html
# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html