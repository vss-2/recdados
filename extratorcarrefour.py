from bs4 import BeautifulSoup
import csv
from json import load
import codecs
from bs4 import BeautifulSoup
from os.path import exists

def main():
    cs = None
    with open('carrefour.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Marca", "Tamanho", "Tecnologia", "Tela", "Entradas", "Dominio", "arquivo","title"])
        for y in range(1089):
            print(y)
            if exists("carrefour/{}.html".format(y)):
                f=codecs.open("carrefour/{}.html".format(y), 'r', 'utf-8')
                document= BeautifulSoup(f.read(), 'html.parser')
                polegadas = document.findAll("span", {"data-specification-name": "Polegadas"})
                tecnologia = document.findAll("span", {"data-specification-name": "Tecnologia da Tela"})
                tela = document.findAll("span", {"data-specification-name": "Resolução da Tela"})
                row = ["","","","","","carrefour","{}.html".format(y), document.title.text]
                row[0] = "null"
                row[4] = "null"
                if(len(polegadas)>0):
                    row[1] = polegadas[1].text
                if(len(tecnologia)>0):
                    row[2] = tecnologia[1].text
                if(len(tela)>0):
                    row[3] = tela[1].text
                if(not "" in row):
                    writer.writerow(row)
    return

if __name__ == "__main__":
    main()