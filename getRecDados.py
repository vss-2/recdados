from random import randint
from csv import reader

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
