from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from time import sleep
import re
from json import load

def main():
    cs = None
    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    #options.add_argument('window-size: 1920x1080')
    driver = webdriver.Chrome(options=options)
    with open("robotsSites.json", "r") as read_file:
        robotstxt = load(read_file)
    
    with open('sites.csv', 'r') as arqcsv:
        reader = csv.reader(arqcsv, delimiter = ',')
        rows = list(reader)
        linkslist = rows[0]
        visitedlist = []
        for k in linkslist:
            count = 0
            while (count < 1000):
                count += 1    
                sitelinks = []
                sitelinks.append((k,1))   
                driver.get(sitelinks[count])
                page = driver.page_source
                soup = BeautifulSoup(page, 'html.parser')
                #for link in soup.find_all('a'):
                #    print(link.get('href'))
    return
def filter(link) -> bool:
    disallowCheck()
    alreadyVisited()
    

def disallowCheck() -> bool: 
    x = 0
def alreadyVisited() -> bool: 
    x = 0
def regularExpression(expr, str) -> bool:   
    result = re.search(expr, str)
    if result == None:
        return True
    return False    
if __name__ == "__main__":
    main()