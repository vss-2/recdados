from bs4 import BeautifulSoup
import csv
from json import load
import codecs
from bs4 import BeautifulSoup
from os.path import exists

def main():
    cs = None
    with open('colombo.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Marca", "Tamanho", "Tecnologia", "Tela", "Entradas", "Dominio","arquivo","title"])
        for y in range(2000):
            print(y)
            if exists("colombo/{}.html".format(y)):
                f=codecs.open("colombo/{}.html".format(y), 'r', 'utf-8')
                document= BeautifulSoup(f.read(), 'html.parser')
                marca = document.findAll("div", {"class": "caracteristicas-fabricante-item"})
                left = document.findAll("div", {"class": "caracteristicas-label"})
                right = document.findAll("div", {"class": "caracteristicas-description"})
                row = ["","","","","null","Colombo","{}.html".format(y), document.title.text]
                if(len(marca)>0):
                    row[0] = marca[0].text
                for x in range(len(left)):
                    if(left[x].text == "Tela:"):
                        row[1] = right[x].text
                    if(left[x].text == "Tipo de tela:"):
                        row[2] = right[x].text
                    if(left[x].text == "Resolução:"):
                        row[3] = right[x].text
                    #if(left[x].text == "Conexões"):
                    #   row[4] = right[x].text
                if(not "" in row):
                    writer.writerow(row)
    return

if __name__ == "__main__":
    main()