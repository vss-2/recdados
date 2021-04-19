#%%
from pickle import load, dump
from bs4 import BeautifulSoup
from os.path import exists

# De acordo com o slide 26 da aula de https://cin.ufpe.br/~luciano/cursos/ri/web_ir.pdf
# Na criação do arquivo invertido temos que ter os 5 pares valor-atributo que mais frequentes
# Creio que esses vão ser os 5 atributos mais frequentes
pares_atributo_valor = ['marca', 'tipo de tela', 'resolução', 'polegadas', 'entradas'] #OBS: Entradas é "confuso", pois existem HDMIs, USBs, componentes, etc
pav = [ set('marca', 'fabricante'), 
        set('tipo da tela', 'tipo de tela', 'tecnologia da tela', 'tecnologia'), 
        set('resolução', 'monitor'),
        set('polegadas', 'pol', 'tamanho da tela'),
        set('entradas', 'entradas laterais', 'entrada lateral', 'entrada traseira', 'entradas traseiras')]
# Tem que montar os pares (será que é pra montar tipo ['marca': ['Samsung', 'LG', 'Sony', 'Semp Toshiba', 'Multilaser']] ???),
# E fazer o mapeamento entre sites (exemplo: 'tamanho de tela' em americanas é 'polegadas' em outro site)

def extrator_americanas():
    return None

def extrator_carrefour():
    # Implementado de forma estranha pela VTex, eles não usam tablets, mas um json próprio pra substituir em spans
    
    # Existe um componente pai do valor atributo, exemplo real coletado:
    # <divpai>
    #         <span data-specification-group="Informações Técnicas" data-specification-name="Tecnologia da Tela" class="vtex-product-specifications-1-x-specificationName">Tecnologia da Tela</span>
    #         <span data-specification-group="Informações Técnicas" data-specification-name="Tecnologia da Tela" data-specification-value="LED" class="vtex-product-specifications-1-x-specificationValue vtex-product-specifications-1-x-specificationValue--first vtex-product-specifications-1-x-specificationValue--last">LED</span>
    # </divpai>
    
    # Teria que coletar para esses outro 4 componentes
    # <span data-specification-group="Importante" data-specification-name="Itens Inclusos" class="vtex-product-specifications-1-x-specificationName">Itens Inclusos</span>
    # <span data-specification-group="Informações Técnicas" data-specification-name="Resolução da Tela" class="vtex-product-specifications-1-x-specificationName">Resolução da Tela</span>
    # <span data-specification-group="Informações do Produto" data-specification-name="Polegadas" class="vtex-product-specifications-1-x-specificationName">Polegadas</span>
    # <span data-specification-group="Conectividade" data-specification-name="Entradas HDMI" class="vtex-product-specifications-1-x-specificationName">Entradas HDMI</span>

def extrator_colombo():
    # Usa modelo de div, exemplo real:
    # <div class="caracteristicas-row">
    #         <div class="caracteristicas-label"><span>Tipo de tela:</span></div>
    #         <div class="caracteristicas-description">
    #             <span>
                    
                        
                        
                        
    #                         LED
                        
                    
                    
    #             </span>
    #         </div>
    #     </div>
    # Uma boa ideia é buscar por caracteristicas-label, limpar o ":", e anexar o description (lembrar de usar .strip() pra tirar espaços em branco da string)

def extrator_gazin():
    # Usa modelo de tabela bastante simplificado, ter cuidado apenas com o &nbsp; no item-campo td na hora de limpar a string
    # <tr class="item"><td class="item-campo">Tecnologia da tela&nbsp;</td><td class="item-valor"><span>LED</span></td></tr>

def extrator_havan():
    # Adiciona diversos <p> sem nenhuma classe dentro de uma div com class="value"
    # <p><strong>Tela:</strong><br>
    # Tamanho da Tela: 50".<br>
    # Display: LCD/LED.<br>
    # Resolução: 3840 x 2160 (4K Ultra HD).<br>
    # Processador: Quad Core.<br>
    # DTV: Sim.<br>
    # HDR10: Sim.<br>
    # Formato Tela: 16:9.<br>
    # Frequência Nativa: 60Hz.</p>

def extrator_kabum():
    # Conteúdo encontra-se na div <div class=3D"content_tab" style=3D"width: 737px;">
    # Insere cada característica em um <p> sem classe, OBS: tem muitos caracteres que não são UTF-8 e aparecem quebrados conexões = Conex=F5es
    # </p><p><strong>Caracter=EDsticas:</strong></p>
    # <p>Marca: Samsung</p>
    # <p>Modelo: LH32BETBLGGXZD</p>
    # <p>&nbsp;</p>
    # <p><strong>Especifica=E7=F5es:</strong></p>
    # <p><strong><br></strong></p>
    # <p><strong>Tela:</strong></p>
    # <p>- Tamanho: 32" HD</p>
    # <p>- Brilho (T=EDpico): 250nit</p>
    # <p>- Contraste (Tipico): 4,700:1</p>
    # <p>- Angulo de Vis=E3o (HxV): 178:178</p>
    # <p>- Opera=E7=E3o: 8/7</p>
    # <p>&nbsp;</p>
    # <p><strong>Conex=F5es:</strong></p>
    # <p>- 2 x HDMI</p>
    # <p>- 1 x USB</p>
    # <p>- RF 1 Terrestrial / 1 Cable</p>
    # <p>&nbsp;</p>
    # <p><strong>Conectividade:&nbsp;</strong></p>
    # <p>- RJ45</p>
    # <p>- WiFi</p>
    # <p>&nbsp;</p>
    # <p><strong>Alimenta=E7=E3o:</strong></p>
    # <p>- Energia: AC100-240V &amp; 50/60Hz</p>
    # <p>- Consumo max de energia: 48</p>
    # <p>&nbsp;</p>

def extrator_magazineluiza():
    # Multiplas tabelas que compõem uma tabela só, exemplo real:
    # <table class="description__box--wildSand">
    #   <tbody>
    #     <tr>
    #       <td class="description__information-left">Tecnologia</td>
    #       <td class="description__information-right">
    #         <table class="description__box">
    #           <tbody>
    #             <tr>
    #               <td class="description__information-box-left"></td>
    #               <td class="description__information-box-right">LED</td>
    #             </tr>
    #           </tbody>
    #         </table>
    #       </td>
    #     </tr>
    #   </tbody>
    # </table>



def extrator():
    site = 'americanas'
    a = '1'

    palavras = dict()
    titulos = []

    for _ in range(1,10):
        a = str(_)
        sfatd = None
        if exists('./minerados/db/{}/{}.html'.format(site, a)):
            with open('./minerados/db/{}/{}.html'.format(site, a), 'r') as arqhtml:
                sopa = BeautifulSoup(arqhtml, 'html.parser')
                extraidos = []
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