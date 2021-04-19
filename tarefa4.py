#%%
from pickle import load, dump
from bs4 import BeautifulSoup
from os.path import exists

# De acordo com o slide 26 da aula de https://cin.ufpe.br/~luciano/cursos/ri/web_ir.pdf
# Na criação do arquivo invertido temos que ter os 5 pares valor-atributo que mais frequentes
# Creio que esses vão ser os 5 atributos mais frequentes
pares_atributo_valor = ['marca', 'tipo de tela', 'resolução', 'polegadas', 'entradas']
# Tem que montar os pares (será que é pra montar tipo ['marca': ['Samsung', 'LG', 'Sony', 'Semp Toshiba', 'Multilaser']] ???),
# E fazer o mapeamento entre sites (exemplo: 'tamanho de tela' em americanas é 'polegadas' em outro site)

def extrator_americanas():
    return None

def extrator():
    site = 'americanas'
    a = '1'

    element = ['script', 'style', 'noscript', 'img', 'input', 'br', 'option', 'form', 'polygon', 'svg']

    palavras = dict()
    titulos = []

    for _ in range(1,10):
        a = str(_)
        sfatd = None
        if exists('./minerados/db/{}/{}.html'.format(site, a)):
            with open('./minerados/db/{}/{}.html'.format(site, a), 'r') as arqhtml:
                sopa = BeautifulSoup(arqhtml, 'html.parser')
                extraidos = []
                for e in element:
                    for sfa in sopa.findAll(e):
                        sopa.extract()
                sfatd = sopa.findAll('title')
                titulos.append(sfatd[0].text.lower())
                sfatd = sopa.findAll('td')
                for s in sfatd:
                    if(s.text in palavras.keys()):
                        palavras[s.text].add(a)
                    else:
                        palavras.update({s.text.lower(): set({a})})
                # print(s.text)
    # Palavras são conteúdos da tabela da página
    return [palavras, titulos]

# Segundo slide 12 em https://cin.ufpe.br/~luciano/cursos/ri/ranking.pdf
# Temos que ter um Learning to Rank (L2R)
# Dividimos em coleções e damos peso aos componentes: título e corpo (ACHO QUE SÓ DÁ PRA FAZER DELES)

def avaliarTituloCorpo(busca, titulo, corpo):
    try:
        if titulo != None:
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
            if('+' in titulo):
                titulo = titulo.replace('+', ' ')
            
            titulo = titulo.casefold().split(' ')

    except Exception as e:
        # print('Houve um problema no minerador() durante a avaliacao do score do titulo')
        pass

def learning_to_rank(busca):
    # Busca estilo: "tv samsung 49 polegadas"
    busca = busca.split(' ')
    learning_to_rank = []

    buscas = [
                extrator_americanas()
            ]

    for site in buscas:
        # score de busca e corpo se tiver pelo menos uma correspondência, é 1
        # creio eu que tem que fazer com os 5 pares atributo-valor (senão fica mto fraca a busca)
        sc_corpo = any([b in busca for b in corpo])
        sc_titulo = any([b in busca for b in titulo])
        learning_to_rank.append([sc_corpo, sc_titulo])
    return learning_to_rank

## Para apresentação: tem que calcular o erro total do learning_to_rank
def apresentacao():
    print('Implementar o cálculo de erro total, tem que classificar e fazer treino-teste!')


def tf_idf():
    # Term-Frequency-Inverse-Document-Frequency
    # Conta aparição de cada termo da busca
    # Ao invés de ponderar os mais aparecidos, inverte a lista
    # Pondera com a classificação invertida
    # https://pt.wikipedia.org/wiki/Tf–idf
    print('Implementar o termo-frequencia-por-documento-com-frequencia-inversa')

def postings():
    # Termo visto no slide 26 em https://cin.ufpe.br/~luciano/cursos/ri/ranking.pdf    
    print('Implementar um dos dois: document at a time ou term at a time')

def ranking_cosseno(q):
    # Algoritmo visto no slide 25 em https://cin.ufpe.br/~luciano/cursos/ri/ranking.pdf
    # Suponho que o Q seja uma querry

    #    scores, l = [0]*len(q), [None]*len(q)

    #    for r in q:
    #         calc = ??
    #         scores[d] += wf * w
    #         for d in l:
    #            scores = scores[d]/l[d]
    #   return scores
    print('Implementar ranking de cosseno, necessário antes tf_idf')

necessario_fazer = [apresentacao(), tf_idf(), ranking_cosseno(1)]