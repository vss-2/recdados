from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import sklearn
import optuna
import mlflow

atual = ''

heuristica = False

if heuristica:
    pasta = 'heuristica'
else:
    pasta = 'baseline'

X_treino, X_teste, y_treino, y_teste = train_test_split(m_geral[0], m_geral[1], test_size=0.25, random_state=len(m_geral[0])//2)

def executar_classificador(trial, qual: str = 'nvb'):
    sugestao = trial.suggest_int(name='Classificar site', low=0, high=1)

    if(atual == 'rfc'):
        n_estimadores = trial.suggest_int("rf_n_estimators", 5, 15)
        max_profundidade = trial.suggest_int("rf_max_depth", 2, 16, log=True)
        regressor = sklearn.ensemble.RandomForestClassifier(max_depth=max_profundidade, n_estimators=n_estimadores, random_state=0, n_jobs=-1)
        score = sklearn.model_selection.cross_val_score(regressor, X_treino, y_treino, n_jobs=-1)
    elif(atual == 'mlp'):
        learning_rate_sug = trial.suggest_float("learning_rate", 1e-5, 1e-3, log=True)
        power_t_sug = trial.suggest_int('power_t', 0.8, 0.8, step=0.1)
        regressor = sklearn.ensemble.RandomForestClassifier(max_depth=max_profundidade, n_estimators=n_estimadores, random_state=0)
        score = sklearn.model_selection.cross_val_score(regressor, X_treino, y_treino, n_jobs=-1)
    else:
        exit()
    
    # for passo in range(100):
    #     regressor.fit(x_train, y_train)
    #     valor_intermediario = regressor.score(x_test, y_test)
    #     trial.report(valor_intermediario, passo)

    #     if trial.should_prune():
    #         raise optuna.TrialPruned()
    #     return valor_intermediario
    
    # acuracia = score.mean()
    # return print('Acurácia:',acuracia)

gnb, rfc, mlp, svc, lgr = GaussianNB(), RandomForestClassifier(), MLPClassifier(), SVC(), LogisticRegression()

classificadores = ['rfc', 'mlp']
for c in classificadores:
    atual = c
    estudo = optuna.create_study(direction='maximize')
    estudo.optimize(executar_classificador, n_trials=10)

    # podas_testadas = [et for et in estudo.trials if et.state == optuna.trial.TrialState.PRUNED]
    # completos_testes = [et for et in estudo.trials if et.state == optuna.trial.TrialState.COMPLETE]
    # executar_classificador()


print('Testes encerrados, podados e completos:', len(estudo.trials), len(podas_testadas), len(completos_testes))
