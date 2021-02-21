import requests
from bs4 import BeautifulSoup

def buscaID(sopa, id):
    # Inserir possível tratamento
    return sopa.find(id)

def buscaClasse(sopa, div, classe):
    # Inserir possível tratamento
    return sopa.find(div, class_=classe)

def buscaTagConteudo(sopa, tag, conteudo):
    # Inserir possível tratamento
    return sopa.find(tag, string=conteudo)

def scrapper(busca):
    # Vai baixar da lista do sites.csv
    with open('sites.csv', 'r') as arqcsv:
        linhas = arqcsv.readlines()
        for l in linhas:
            pagina = requests.get(l)
            sopa   = BeautifulSoup(page.content, 'html.parser')
            resultados = dict({'id': None, 'classe': None, 'elementos': None})
            
            if(busca=='id'):
                resultados = buscaID(sopa, id)
            elif(busca=='classe'):
                res1 = buscaClasse(sopa, div, classe)
            elif(busca=='elementos'):
                res
            else:
                res1 = buscaID(sopa, id)
                res2 = buscaClasse(sopa, div, classe)
    return
