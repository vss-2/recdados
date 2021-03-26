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
from feature_selection import selecionar, minerador
from bs4 import BeautifulSoup
from sklearn.metrics import accuracy_score, f1_score, average_precision_score
from sklearn.model_selection import train_test_split
from timeit import default_timer as timer
import warnings
import mlflow
import pandas as pd
import numpy as np
import pickle

warnings.filterwarnings("ignore")

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

    gSL = getSitesLista()

    with open('features.csv', 'r') as arqcsv:
        
        feats = reader(arqcsv, delimiter=',')
        feats = [c for c in feats][0]
        feats.append('Score Titulo')
        feats.append('Score Body')
        m_geral = [[],[]]

        for site in gSL:
            
            # Teste de 5/20
            # print('Executando classificador com partição de rótulos para:', site.capitalize())
            
            m = []
            treino = pd.DataFrame()
            mil = dict()
                        
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


            # df = pd.DataFrame(list(mil.values()), columns = feats)

            um_zero = [1]*(numfeats+1) + [0]*(numfeats+1)

            m_geral[0].extend(m)
            m_geral[1].extend(um_zero)

            with open('./minerados/mil/{}/m_geral'.format(pasta), 'wb') as arqdados:
                pickle.dump(m_geral, arqdados)            

            # Juntar dataframes treino e df caso seja necessário:
            # print(treino.append(df,ignore_index=True))
            # print(df.head())

            # Teste de 5/20
            # X_treino, X_teste, y_treino, y_teste = train_test_split(m, um_zero, test_size=0.25, random_state=len(m)//2)

            # gnb, rfc, mlp, svc, lgr = GaussianNB(), RandomForestClassifier(), MLPClassifier(), SVC(), LogisticRegression()

            # gnb.fit(X_treino, y_treino)
            # result = gnb.predict(X=X_teste)
            # score = gnb.score(X=X_teste, y=y_teste)
            # with open('./minerados/mil/{}/{}/gnb'.format(pasta, site), 'wb') as arqdados:
            #     pickle.dump(result, arqdados)
            # print('Precision, F-Score e Acurácia Naive Bayes: \n', average_precision_score(y_teste, result), f1_score(y_teste, result), score)

            # rfc.fit(X_treino, y_treino)
            # result = rfc.predict(X=X_teste)
            # score = rfc.score(X=X_teste, y=y_teste)
            # with open('./minerados/mil/{}/{}/rfc'.format(pasta, site), 'wb') as arqdados:
            #     pickle.dump(result, arqdados)
            # print('Precision, F-Score e Acurácia Random Forest Classifier: \n', average_precision_score(y_teste, result), f1_score(y_teste, result), score)

            # mlp.fit(X_treino, y_treino)
            # result = mlp.predict(X=X_teste)
            # score = mlp.score(X=X_teste, y=y_teste)
            # with open('./minerados/mil/{}/{}/mlp'.format(pasta, site), 'wb') as arqdados:
            #     pickle.dump(result, arqdados)
            # print('Precision, F-Score e Acurácia Multi-layer Perceptron: \n', average_precision_score(y_teste, result), f1_score(y_teste, result), score)

            # svc.fit(X_treino, y_treino)
            # result = svc.predict(X=X_teste)
            # score = svc.score(X=X_teste, y=y_teste)
            # with open('./minerados/mil/{}/{}/svc'.format(pasta, site), 'wb') as arqdados:
            #     pickle.dump(result, arqdados)
            # print('Precision, F-Score e Acurácia SVC: \n', average_precision_score(y_teste, result), f1_score(y_teste, result), score)

            # lgr.fit(X_treino, y_treino)
            # result = lgr.predict(X=X_teste)
            # score = lgr.score(X=X_teste, y=y_teste)
            # with open('./minerados/mil/{}/{}/lgr'.format(pasta, site), 'wb') as arqdados:
            #     pickle.dump(result, arqdados)
            # print('Precision, F-Score e Acurácia Logistic Regression: \n', average_precision_score(y_teste, result), f1_score(y_teste, result), score)

            # print('Tempo gasto para', site.capitalize(), timer()-tempo_inicial, '\n')
        
        # ------------------------------------------------------------ Recebendo os 200 rótulos -----------------------------------------------------------------
        tempo_inicial = timer()

        # X_treino, y_treino = m_geral[0], m_geral[1]
        X_treino, X_teste, y_treino, y_teste = train_test_split(m_geral[0], m_geral[1], test_size=0.25, random_state=len(m_geral[0])//2)
        print('Somatório de rótulos totalizando:', len(m_geral[0]))

        gnb, rfc, mlp, svc, lgr = GaussianNB(), RandomForestClassifier(n_jobs=-1), MLPClassifier(), SVC(), LogisticRegression(n_jobs=-1)

        gnb.fit(X_treino, y_treino)
        result = gnb.predict(X=X_teste)
        score = gnb.score(X=X_teste, y=y_teste)
        print('Precision, F-Score e Acurácia Naive Bayes: \n', average_precision_score(y_teste, result), f1_score(y_teste, result), score)

        rfc.fit(X_treino, y_treino)
        result = rfc.predict(X=X_teste)
        score = rfc.score(X=X_teste, y=y_teste)
        print('Precision, F-Score e Acurácia Random Forest Classifier: \n', average_precision_score(y_teste, result), f1_score(y_teste, result), score)

        mlp.fit(X_treino, y_treino)
        result = mlp.predict(X=X_teste)
        score = mlp.score(X=X_teste, y=y_teste)
        print('Precision, F-Score e Acurácia Multi-layer Perceptron: \n', average_precision_score(y_teste, result), f1_score(y_teste, result), score)

        svc.fit(X_treino, y_treino)
        result = svc.predict(X=X_teste)
        score = svc.score(X=X_teste, y=y_teste)
        print('Precision, F-Score e Acurácia SVC: \n', average_precision_score(y_teste, result), f1_score(y_teste, result), score)

        lgr.fit(X_treino, y_treino)
        result = lgr.predict(X=X_teste)
        score = lgr.score(X=X_teste, y=y_teste)
        print('Precision, F-Score e Acurácia Logistic Regression: \n', average_precision_score(y_teste, result), f1_score(y_teste, result), score)

        print('Tempo gasto para testar', len(X_teste), 'foi', timer()-tempo_inicial, '\n')  
        # ------------------------------------------------------------ Recebendo os 200 rótulos -----------------------------------------------------------------

        X_treino, y_treino = m_geral[0], m_geral[1]
        dez_mil = []

        for site in gSL:
            
            mil = dict()

            if novos_dados:
                    
                if exists('./minerados/mil/{}/{}/1010.html'.format(pasta, site)):
                    for a in range(1001, 2000):
                        if exists('./minerados/mil/{}/{}/{}.html'.format(pasta, site, a)):
                            with open('./minerados/mil/{}/{}/{}.html'.format(pasta, site, a), 'r') as arqhtml2:
                                sopa = BeautifulSoup(arqhtml2, 'html.parser')
                                k = minerador(sopa, feats)
                                mil.update({len(mil)+len(m):k})
                                dez_mil.append(k)
                else:
                    # Lê os 1000 htmls da loja específica
                    for a in range(1, 1000):
                        if exists('./minerados/mil/{}/{}/{}.html'.format(pasta, site, a)):
                            with open('./minerados/mil/{}/{}/{}.html'.format(pasta, site, a), 'r') as arqhtml2:
                                sopa = BeautifulSoup(arqhtml2, 'html.parser')
                                k = minerador(sopa, feats)
                                mil.update({len(mil)+len(m):k})
                                dez_mil.append(k)

                with open('./minerados/mil/{}/{}/mil'.format(pasta, site), 'wb') as arqdados:
                    pickle.dump(mil, arqdados)
                
                with open('./minerados/mil/dez_mil', 'wb') as arqdados:
                    pickle.dump(dez_mil, arqdados)

            else:
                if exists('./minerados/mil/{}/{}/mil'.format(pasta, site)):
                    with open('./minerados/mil/{}/{}/mil'.format(pasta, site), 'rb') as arqdados:
                        mil = pickle.load(arqdados)                
                else:
                    print('Arquivo mil não encontrado, tente rodar com o parâmetro novos_dados = True')
                    exit()
                
                if exists('./minerados/mil/dez_mil'):
                    with open('./minerados/mil/dez_mil', 'rb') as arqdados:
                        dez_mil = pickle.load(arqdados)                
                else:
                    print('Arquivo dez_mil não encontrado, tente rodar com o parâmetro novos_dados = True')
                    exit()

            tempo_inicial = timer()
            
            # Recebendo os 1000 htmls
            X_teste = mil.values()

            gnb, rfc, mlp, svc, lgr = GaussianNB(), RandomForestClassifier(n_jobs=-1), MLPClassifier(), SVC(), LogisticRegression(n_jobs=-1)
            harvest = [0,0,0,0,0]

            for tst in X_teste:
                gnb.fit(X_treino, y_treino)
                result = gnb.predict(X=[tst])
                harvest[0] += result[0]

                rfc.fit(X_treino, y_treino)
                result = rfc.predict(X=[tst])
                harvest[1] += result[0]

                mlp.fit(X_treino, y_treino)
                result = mlp.predict(X=[tst])
                harvest[2] += result[0]

                svc.fit(X_treino, y_treino)
                result = svc.predict(X=[tst])
                harvest[3] += result[0]

                lgr.fit(X_treino, y_treino)
                result = lgr.predict(X=[tst])
                harvest[4] += result[0]
            
            print('Resultados Harvest usando {} rótulos para os {} htmls de {} \nNaive Bayes: {} \nRandom Forest: {} \nMulti-layer Perceptron: {} \nSVC: {} \nLinear Regression: {}'.format(len(X_treino), len(mil), site.capitalize(), harvest[0], harvest[1], harvest[2], harvest[3], harvest[4]))
            print('Tempo gasto nos classificadores para', site.capitalize(), timer()-tempo_inicial, '\n')

        tempo_inicial = timer()
        
        # Recebendo os 10000 htmls
        X_teste = dez_mil

        gnb, rfc, mlp, svc, lgr = GaussianNB(), RandomForestClassifier(n_jobs=-1), MLPClassifier(), SVC(), LogisticRegression(n_jobs=-1)
        harvest = [0,0,0,0,0]

        for tst in X_teste:
            gnb.fit(X_treino, y_treino)
            result = gnb.predict(X=[tst])
            harvest[0] += result[0]

            rfc.fit(X_treino, y_treino)
            result = rfc.predict(X=[tst])
            harvest[1] += result[0]

            mlp.fit(X_treino, y_treino)
            result = mlp.predict(X=[tst])
            harvest[2] += result[0]

            svc.fit(X_treino, y_treino)
            result = svc.predict(X=[tst])
            harvest[3] += result[0]

            lgr.fit(X_treino, y_treino)
            result = lgr.predict(X=[tst])
            harvest[4] += result[0]
        
        print('Resultados Harvest usando {} rótulos para {} htmls vindos de todos os sites \nNaive Bayes: {} \nRandom Forest: {} \nMulti-layer Perceptron: {} \nSVC: {} \nLinear Regression: {}'.format(len(X_treino), len(dez_mil), harvest[0], harvest[1], harvest[2], harvest[3], harvest[4]))
        print('Tempo gasto nos classificadores para avaliar todos os sites', timer()-tempo_inicial, '\n')
        

classificador(novos_dados=False, heuristica=False)
