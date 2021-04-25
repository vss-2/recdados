from bs4 import BeautifulSoup
import csv
from json import load
import codecs
from bs4 import BeautifulSoup
from os.path import exists

def main():
    cs = None
    with open('amazon.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Marca", "Tamanho", "Tecnologia", "Tela", "Entradas", "Dominio", "arquivo","title"])
        for y in range(1089):
            print(y)
            if exists("amazon/{}.html".format(y)):
                f=codecs.open("amazon/{}.html".format(y), 'r', 'utf-8')
                document= BeautifulSoup(f.read(), 'html.parser')
                left = document.findAll("th", {"class": "a-color-secondary a-size-base prodDetSectionEntry"})
                right = document.findAll("td", {"class": "a-size-base prodDetAttrValue"})
                row = ["","","","","","Amazon","{}.html".format(y), document.title.text]
                for x in range(len(left)):
                    
                    if "Marca" in left[x].text:
                        row[0] = right[x].text
                    if"Tamanho da tela" in left[x].text:
                        row[1] = right[x].text
                    if "Tela ou mostrador" in left[x].text:
                        row[2] = right[x].text
                    if "Resolução" in left[x].text:
                        row[3] = right[x].text
                    if "Tecnologia de conexão" in left[x].text:
                        row[4] = right[x].text
                if(not "" in row):
                    writer.writerow(row)
    return

if __name__ == "__main__":
    main()