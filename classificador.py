import re

def classificador() -> int:
    score = 1

    separadores = {0: '-', 1: '_'}

    link = str(input()).casefold()
    identificar = []

    for i in separadores:
        identificar.append(link.count(separadores[i]))

    link_bkp = link
    slpsep = separadores[identificar.index(max(identificar))]
    link = link.split(slpsep)

    for l in link:
        if('led' in link or 'lcd' in link or 'oled' in link or 'qled' in link):
            score *= 2
            try:
                if 'led' in link:
                    link.remove('led')
                if 'lcd' in link:
                    link.remove('lcd') 
                if 'oled' in link:
                    link.remove('oled') 
                if 'qled' in link:
                    link.remove('qled')
            except:
                pass
        if('4k' in link or 'uhd' in link or 'hd' in link or ('full' in link and 'hd' in link)):
            score *= 2
            try:
                if '4k' in link:
                    link.remove('4k')
                if 'uhd' in link:
                    link.remove('uhd')
                if 'hd' in link:
                    link.remove('hd')
                if ('full' in link and 'hd' in link):
                    link.remove('full')
                    link.remove('hd')
            except:
                pass
        try:
            # Removendo polegadas pela expressão regular
            valor = re.search(slpsep+'[0-9]{2}'+slpsep, link_bkp)
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
    