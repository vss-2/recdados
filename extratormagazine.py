from bs4 import BeautifulSoup
import csv
from json import load
import codecs
from bs4 import BeautifulSoup
from os.path import exists

def main():
    cs = None
    with open('magazine.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Marca", "Tamanho", "Tecnologia", "Tela", "Entradas", "Dominio", "arquivo","title"])
        for y in range(1089):
            print(y)
            if exists("magazine/{}.html".format(y)):
                f=codecs.open("magazine/{}.html".format(y), 'r', 'utf-8')
                document= BeautifulSoup(f.read(), 'html.parser')
                left = document.findAll("td", {"class": "description__information-left"})
                right = document.findAll("td", {"class": "description__information-right"})
                row = ["","","","","","Magazine Luiza","{}.html".format(y), document.title.text]
                for x in range(len(left)):
                    if(left[x].text == "Informações técnicas"):
                        row[0] = right[x].text
                    if(left[x].text == "Polegadas"):
                        row[1] = right[x].text
                    if(left[x].text == "Tecnologia"):
                        row[2] = right[x].text
                    if(left[x].text == "Tela"):
                        row[3] = right[x].text
                    if(left[x].text == "Conexões"):
                        row[4] = right[x].text
                if(not "" in row):
                    writer.writerow(row)
    return

if __name__ == "__main__":
    main()