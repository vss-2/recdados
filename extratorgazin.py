from bs4 import BeautifulSoup
import csv
from json import load
import codecs
from bs4 import BeautifulSoup
from os.path import exists

def main():
    cs = None
    with open('gazin.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Marca", "Tamanho", "Tecnologia", "Tela", "Entradas", "Dominio", "arquivo","title"])
        for y in range(1089):
            print(y)
            if exists("gazin/{}.html".format(y)):
                f=codecs.open("gazin/{}.html".format(y), 'r', 'utf-8')
                document= BeautifulSoup(f.read(), 'html.parser')
                left = document.findAll("td", {"class": "item-campo"})
                right = document.findAll("td", {"class": "item-valor"})
                print(document.title)
                if(document.title != None):
                    titl = document.title.text
                row = ["","","","","null","Gazin","{}.html".format(y), titl]
                for x in range(len(left)):
                    if(left[x].text == "Marca"):
                        row[0] = right[x].text
                    if(left[x].text == "Tamanho da tela"):
                        row[1] = right[x].text
                    if(left[x].text == "Tecnologia da tela"):
                        row[2] = right[x].text
                    if(left[x].text == "Resolução"):
                        row[3] = right[x].text
                    if(left[x].text == "Conexões"):
                        row[4] = right[x].text
                if(not "" in row):
                    writer.writerow(row)
    return

if __name__ == "__main__":
    main()