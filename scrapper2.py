import requests
from getHeaders import getHeaders
from os import listdir
from bs4 import BeautifulSoup

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
    main()