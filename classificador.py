import re
from getRecDados import getBagOfWords

def classificador(texto: str = '') -> int:
    if texto == '':
        return 0

    texto = texto.casefold()

    for x in ['-', '_', ',', '/']:
        texto = texto.replace(x, ' ')

    texto_sp = texto.split(' ')
    texto_sp = [k.strip() for k in texto_sp]

    bow = getBagOfWords()

    score = 1

    for b in bow:
        if b in texto_sp:
            score *= 2

    try:
        # Removendo polegadas pela expressão regular
        valor = re.search('[0-9]{2}', texto)
        # print(valor, splsep, link_bkp)
        print(valor.regs)
        if(valor.regs):
            # print(str(link_bkp[valor.regs[0][0]+1:valor.regs[0][1]-1]))
            # print(link)
            # link.remove(str(link_bkp[valor.regs[0][0]+1:valor.regs[0][1]-1]))
            score *= 2
    except:
        pass

    return score

if __name__ == '__main__':
    print(classificador())
