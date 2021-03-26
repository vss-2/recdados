from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from timeit import default_timer as timer
import mlflow
import numpy as np
import pickle
import optuna
from optuna.integration.mlflow import MLflowCallback
import sklearn
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import warnings
warnings.filterwarnings("ignore")


with open('./minerados/mil/baseline/m_geral', 'rb') as arqdados:
    m_geral = pickle.load(arqdados)

X_treino, X_teste, y_treino, y_teste = train_test_split(m_geral[0], m_geral[1], test_size=0.25, random_state=len(m_geral[0])//2)

def executar_classificador(trial):
    sugestao = trial.suggest_int(name='Classificar site', low=0, high=1)
    n_estimadores = trial.suggest_int("n_estimators", low=5, high=15)
    max_profundidade = trial.suggest_int("max_depth", low=2, high=16, log=True)

    classifica = RandomForestClassifier(max_depth=max_profundidade, n_estimators=n_estimadores, random_state=0, n_jobs=-1)
    classifica.fit(X_treino, y_treino)
    score = classifica.score(X_teste, y_teste)
    # print(score)
    return score

def executar_classificador2(trial):
    sugestao = trial.suggest_int(name='Classificar site', low=0, high=1)
    learning_rate_sug = trial.suggest_float("learning_rate", low=1e-5, high=1e-3, log=True)
    power_t_sug = trial.suggest_float('power_t', low=0.5, high=0.9, step=0.1)

    classifica = MLPClassifier(power_t=power_t_sug, learning_rate_init=learning_rate_sug, random_state=0)
    classifica.fit(X_treino, y_treino)
    score = classifica.score(X_teste, y_teste)
    # print(score)
    return score

tempo_inicial = timer()
print('Iniciando Random Florest')
study = optuna.create_study(direction="maximize")
study.optimize(executar_classificador, n_trials=100)
print('\n\n\nTempo de execução do Random Florest:', timer()-tempo_inicial)

tempo_inicial = timer()
print('Iniciando Multilayer Perceptron')
study2 = optuna.create_study(direction="maximize")
study2.optimize(executar_classificador2, n_trials=100)
print('\n\n\nTempo de execução do Multilayer Perceptron:', timer()-tempo_inicial)

mlflow_retorno = MLflowCallback(
    tracking_uri = 'mlruns',
    metric_name  = 'fit'
)

mlflow_retorno2 = MLflowCallback(
    tracking_uri = 'mlruns',
    metric_name  = 'fit'
)

def mlflow_classificador(trial):
    sugestao = trial.suggest_int(name='Classificar site', low=0, high=1)
    n_estimadores = trial.suggest_int("n_estimators", low=5, high=15)
    max_profundidade = trial.suggest_int("max_depth", low=2, high=16, log=True)

    clf = Pipeline(steps=[('scaler', StandardScaler()),
                        ('classifier', RandomForestClassifier(max_depth=max_profundidade, 
                        n_estimators=n_estimadores, random_state=0, n_jobs=-1))])
    clf.fit(X_treino, y_treino)
    score = clf.score(X_teste, y_teste)
    # print(score)
    return score

def executar_classificador2(trial):
    sugestao = trial.suggest_int(name='Classificar site', low=0, high=1)
    learning_rate_sug = trial.suggest_float("learning_rate", low=1e-5, high=1e-3, log=True)
    power_t_sug = trial.suggest_float('power_t', low=0.5, high=0.9, step=0.1)

    clf = Pipeline(steps=[('scaler', StandardScaler()),
                        ('classifier', MLPClassifier(power_t=power_t_sug, 
                        learning_rate_init=learning_rate_sug, random_state=0))])
    clf.fit(X_treino, y_treino)
    score = clf.score(X_teste, y_teste)
    # print(score)
    return score

tempo_inicial = timer()
print('Iniciando Random Florest - MLflow')
study = optuna.create_study(direction="maximize")
study.optimize(executar_classificador, n_trials=100, callbacks=[mlflow_retorno])
print('\n\n\nTempo de execução do Random Florest MLflow:', timer()-tempo_inicial)

tempo_inicial = timer()
print('Iniciando Multilayer Perceptron - MLflow')
study2 = optuna.create_study(direction="maximize")
study2.optimize(executar_classificador2, n_trials=100, callbacks=[mlflow_retorno2])
print('\n\n\nTempo de execução do Multilayer Perceptron MLflow:', timer()-tempo_inicial)
