from bs4 import BeautifulSoup
import csv
from selenium import webdriver
def main():
    cs = None
    with open('sites.csv', 'r') as arqcsv:
        linhas = csv.reader(arqcsv, delimiter = ',')
        # print(next(iter(linhas)))
        for k in linhas:
            print(k)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size: 1920x1080')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("https://twitter.com/search?f=tweets&vertical=default&q=javascript")
        
    return

if __name__ == "__main__":
    main()