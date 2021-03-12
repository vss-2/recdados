from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from getRecDados import getRotulos

def selecaoFeatures(n: int = 5) -> list:
    rot = getRotulos()
    n_melhores = SelectKBest(score_func = f_classif, k = n)
    
    # X,y 
    fit = f_classif.fit()
    # X
    feats = fit.transform()

    print(feats)