import requests
import json
from random import randint
from time import sleep
from getHeaders import getHeaders
from os import listdir, mkdir
from os.path import curdir, isdir, exists
from bs4 import BeautifulSoup

def popular_db() -> None:
    js = None
    
    with open('10_exemplos_positivos_e_negativos.json') as arqjson:
        js = json.load(arqjson)

    for chave in js:
        if not exists(curdir+'/'+ str(chave.split('.')[0])):
            mkdir(chave.split('.')[0])

    for chave in js:
        for valor in js[chave]['positivos']:
            if not exists(curdir+'/'+str(chave.split('.')[0]+'/'+'{}.html'.format(valor))):
                with open('{}/{}.html'.format(chave.split('.')[0], valor), 'w') as arqhtml:
                    output_get = requests.get(url=js[chave]['positivos'][valor], headers=getHeaders())
                    arqhtml.write(output_get.text)
                    sleep(randint(15,40))
            print(chave)

    return None

def main() -> None:
    i = input('Insira o link: ')
    e = input('Exemplo ou DB (e/d): ')
    
    if(e=='d'):
        exit()
    elif(e=='e'):
        with open('minerados/exs/{}.html'.format(len(listdir('/home/vitor/Github/recdados/minerados/exs'))), 'w') as arqhtml:
            result = requests.get(url = i, headers = getHeaders())
            arqhtml.write(result.text)
            s = BeautifulSoup(result.content, 'html.parser')
            arqhtml.write(str(s.find('tbody', recursive=False)))
            arqhtml.close()
    return None

if __name__ == '__main__':
    # main()
    popular_db()