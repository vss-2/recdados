from bs4 import BeautifulSoup
from csv import reader
from getRecDados import getPalavrasRem
from unicodedata import normalize

def featureSelection():

    sites = ['americanas', 'carrefour', 'casasbahia', 'colombo', 'extra', 
    'gazin', 'havan', 'magazineluiza', 'mercadolivre', 'ricardoeletro', 'submarino']

    dados = []
    for s in sites:
        for n in range(1,10):
            sopa = BeautifulSoup(open('/home/vitor/Github/recdados/minerados/db/{}/{}.html'.format(s, n)).read(), features='html.parser')
            
            # fa = sopa.find_all('table')
            # for f in fa:
                # dados.extend(f)
            
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
                    
                    titulo = titulo.casefold().split(' ')

                    for p in getPalavrasRem():
                        if p in titulo:
                            titulo.remove(p)

                    titulo = [t.strip() for t in titulo]
                    
                    dados.extend(titulo)
            except:
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
                    arqcsv.write(str(valor)+': '+str(dados.count(valor))+'\n')
                    s.remove(valor)
            except:
                print(valor)
                pass

    return 

def featureSelecionadas(n: int = 10):
    with open('feature_selection.csv', 'r') as arqcsv:
        leitor = reader(arqcsv, delimiter='\n')
        topfeats = [(l[0].split(': ')[0], int(l[0].split(': ')[1])) for l in leitor]
        topfeats.sort(key=lambda x: x[1])
        # print(topfeats)
        print(topfeats[-n:])
    return

if __name__ == '__main__':
    featureSelection()
    featureSelecionadas()
    exit()