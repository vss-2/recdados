from sklearn.model_selection import train_test_split
from numpy import reshape, array
from numpy.random import shuffle
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from getRecDados import getRotulos

def selecaoFeatures(n: int = 5, loja: int = 0) -> list:
    rot = getRotulos()

    """
        Aqui eu tenho que splitar as URLs em busca de fazer uma lista de 
        palavras relevantes (labels) e valores correspondentes de cada
        string para que o classificador possa trabalhar.
    """

    rot_p = rot[0][loja:10]
    rot_n = rot[1][loja:10]

    treino = [1 if x < (len(rot_n)+len(rot_p))//2 else 0 for x in range(len(rot_n)+len(rot_p))]
    gnb = GaussianNB()

    tst = rot_p+rot_n
    tst = [[x,y] for x in tst for y in treino]

    print([len(treino)], len(rot_p+rot_n))
    gnb.fit(X=array(treino).reshape(-1,1), y=rot_p+rot_n)
    
    k = rot[1][loja+10:loja+20]+rot[1][loja+20:loja+30]
    # shuffle(k)

    tst = [[x,y] for x in k for y in treino]
    # print(tst)
    gnb.predict(X=array(treino).reshape(-1,1))
    # print(gnb.predict(X=k))
    # print(gnb.score(X=array(treino).reshape(-1,1), y=k))


    # pdc = gnb.predict(k)
    # print('Porra:', pdc)
    return [None]

if __name__ == "__main__":
    selecaoFeatures()