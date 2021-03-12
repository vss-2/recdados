import re
from getRecDados import getBagOfWords

def classificador() -> int:
    score = 1

    separadores = {0: '-', 1: '_', 2: ' ', 3: '/'}

    link = str(input()).casefold().replace('\'','').replace('\"','')
    identificar = []

    for i in separadores:
        identificar.append(link.count(separadores[i]))  

    link_bkp = link
    splsep = separadores[identificar.index(max(identificar))]
    # Pode ser interessante aplicar sucessivos splits em separadores
    link = link.split(splsep)

    bow = getBagOfWords()

    while any(x in bow for x in link):
        if 'tv' in link and 'smart' in link:
            link.remove('smart')
            link.remove('tv')
            score *= 2
        if 'led' in link:
            link.remove('led')
            score *= 2
        if 'lcd' in link:
            link.remove('lcd')
            score *= 2
        if 'oled' in link:
            link.remove('oled')
            score *= 2
        if 'qled' in link:
            link.remove('qled')
            score *= 2
        if '4k' in link:
            link.remove('4k')
            score *= 2
        if 'uhd' in link:
            link.remove('uhd')
            score *= 2
        if 'hd' in link:
            link.remove('hd')
            score *= 2
        if ('full' in link and 'hd' in link):
            link.remove('full')
            link.remove('hd')
            score *= 2
        if ('fhd' in link):
            link.remove('fhd')
            score *= 2
        if ('resolucao' in link):
            link.remove('resolucao')
            score *= 2
    
    try:
        # Removendo polegadas pela expressão regular
        valor = re.search(splsep+'[0-9]{2}'+splsep, link_bkp)
        print(valor, splsep, link_bkp)
        # print(valor.regs)
        if(valor.regs):
            # print(str(link_bkp[valor.regs[0][0]+1:valor.regs[0][1]-1]))
            # print(link)
            link.remove(str(link_bkp[valor.regs[0][0]+1:valor.regs[0][1]-1]))
            score *= 2
    except:
        pass

    return score

if __name__ == '__main__':
    print(classificador())
    