from random import randint
from json import load
from csv import reader
from time import sleep
from requests import get
from os.path import exists
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def getSitesLista() -> list:
    return ['amazon', 'mercadolivre', 'casasbahia', 'americanas', 'magazineluiza', 
        'havan', 'gazin', 'extra', 'submarino', 'ricardoeletro', 'carrefour', 'colombo'] 

def getPalavrasRem(remPol: bool = True) -> set:
    # Palavras removidas
    s = set({'', ' ', 'a', 'à', 'e', 'in', 'sem', 'com', 'de', 'do', 'da', 'para', 
    'no', 'na', 'nos', 'nas', 'novo', 'nova', 'americanas', 'carrefour', 'casasbahia', 'colombo', 'extra', 
    'gazin', 'havan', 'magazine', 'magazineluiza', 'luiza', 'mercado', 'mercadolivre', 'livre', 'ricardo eletro', 'submarino'})
    if remPol:
        for num in range(0,100):
            s.add(str(num))
            s.add(str(num)+'\"')
            s.add(str(num)+'”')
            s.add(str(num)+'\'')
            s.add(str(num)+'\'\'')
    return s

def getRotulos(arq: str = '10_exemplos_positivos_e_negativos.json') -> list:
    js = None
    p, n = [], []
    with open('10_exemplos_positivos_e_negativos.json', 'r') as arqjson:
        js = load(arqjson)
        for chave in js:
            for valor in js[chave]['positivos']:
                p.append(js[chave]['positivos'][valor])
            for valor in js[chave]['negativos']:
                n.append(js[chave]['negativos'][valor])
    return [p,n]

def getRobotsDir(site: str, permissao: str = 'disallow') -> list:
    j = None
    with open('robotsSites.json', 'r') as arqjson:
        j = load(arqjson)
    return j[site][permissao]

def getBagOfWords() -> list:
    output = None
    # Obs: qualquer edição no bag of words deverá
    # envolver alteração nos ifs do classificador
    with open('bag_of_words.csv', 'r') as arqcsv:
        c = reader(arqcsv, delimiter=',')
        output = [l for l in c]
    return output[0]

def getRobots(s:str) -> list:
    link = {
        'amazon.com.br': '',
        'mercadolivre.com.br': '',
        'casasbahia.com.br': '',
        'americanas.com.br': '',
        'magazineluiza.com.br': '',
        'havan.com.br': '',
        'gazin.com.br': '',
        'extra.com.br': '',
        'submarino.com.br': '',
        'ricardoeletro.com.br': '',
        'carrefour.com.br': '',
        'colombo.com.br': ''
    }
    return link[s]

def getHeaders() -> dict:
    d = [
        {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 OPR/74.0.3911.144'},
        {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3831.0 Safari/537.36 Edg/77.0.200.1'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3790.0 Safari/537.36'},
        {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.36 Safari/537.36'},
        {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'}
    ]
    return d[randint(0, len(d)-1)]

def getSitesTerminal(posneg: str = 'pos', selenium: bool = True):
    if posneg == 'pos':
        nstart, nend = 1,11
        pn = 0
    else:
        nstart, nend = 11,21
        pn = 1
    
    sites = getSitesLista()
    rot = getRotulos()[0] if posneg == 'pos' else getRotulos()[1]
    
    options, driver = None, None
    if selenium:
        options = Options()
        options.binary_location = '/usr/bin/brave-browser'
        options.add_argument("--enable-javascript")
        driver = webdriver.Chrome(options=options, executable_path='/usr/local/bin/chromedriver')

    for s in sites:
        print(s)
        for n in range(nstart, nend):
            f = n-10 if nstart > 10 else n
            f -= 1
            # print(rot[f])
            if selenium:
                    if not exists('./minerados/db/{}/{}.html'.format(s, n)):
                        driver.get(rot[f])
                        with open('./minerados/db/{}/{}.html'.format(s, n), 'w') as arqhtml:
                            arqhtml.write(driver.page_source)
                            arqhtml.close()
                            sleep(8)
                            driver.execute_script("window.home();")
                            sleep(2)
            else:
                if not exists('./minerados/db/{}/{}.html'.format(s, n)):
                    with open('./minerados/db/{}/{}.html'.format(s, n), 'w') as arqhtml:
                        result = get(url = rot[f], headers = getHeaders())
                        arqhtml.write(result.text)
                        arqhtml.close()
                        sleep(60)
            print(n, sep=' ', end='\n')

    return
