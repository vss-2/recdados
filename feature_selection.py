from bs4 import BeautifulSoup
from csv import reader
from getRecDados import getPalavrasRem, getSitesLista
from unicodedata import normalize
import zipfile

def featureSelection(posneg: str = 'pos', contar: bool = False):

    sites = getSitesLista()

    if posneg == 'pos':
        nstart, nend = 1,11
    else:
        nstart, nend = 11,21

    dados = []
    for s in sites:
        for n in range(nstart, nend):
            try:
                sopa = BeautifulSoup(open('/home/vitor/Github/recdados/minerados/db/{}/{}.html'.format(s, n)).read(), features='html.parser')
            except FileNotFoundError:
                try: 
                    with zipfile.ZipFile('./10_sites_de_cada_exemplo.zip', 'r') as arqzip:
                        arqzip.extractall('./minerados/db/')
                except:    
                    print('Pasta \'minerados/db/\' faltando, favor deszipar o arquivo \'10_sites_de_cada_exemplo.zip\' dentro dela')
                    exit()
            
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
                    if contar:
                        arqcsv.write(str(valor)+': '+str(dados.count(valor))+'\n')
                    else:
                        arqcsv.write(str(valor)+'\n')
                    s.remove(valor)
            except:
                print(valor)
                pass

    return 

def featureSelecionadas(n: int = 10, contar: bool = False):
    with open('feature_selection.csv', 'r') as arqcsv:
        leitor = reader(arqcsv, delimiter='\n')
        if contar:
            topfeats = [(l[0].split(': ')[0], int(l[0].split(': ')[1])) for l in leitor]
            topfeats.sort(key=lambda x: x[1])
        else:
            topfeats = [l[0].split(': ')[0] for l in leitor]
        # print(topfeats)
        print(topfeats[-n:])
    return

if __name__ == '__main__':
    featureSelection()
    featureSelecionadas()
    exit()