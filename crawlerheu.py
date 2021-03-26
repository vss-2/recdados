import json
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from time import sleep
import re
from json import load
from getRecDados import getBagOfWords, getTagsRem
from classificador import classificador
from random import randint
from os.path import exists

def filtroGuiado(soup):
    a_com_link = soup.findAll('a', href=True)
    sitesAvisitar = []

    for acl in a_com_link:
        try:
            k = acl.get('href')
            link_a_class = ' '.join(str(k).casefold().split())
            notalink = classificador(link_a_class)
            notatexto = classificador(acl.text)
            nota = notalink + notatexto
            nota = nota / 2
            if (notalink + notatexto) > 1:
                sitesAvisitar.insert(0, (k, nota))
        except Exception as e:
            # print(e)
            pass

    return sorted(sitesAvisitar, key=lambda x:x[1], reverse=True)

def main():
    with open("robotsSites.json", "r") as read_file:
        robotstxt = load(read_file)

    vitorPC = False
    if vitorPC:
        options = webdriver.ChromeOptions()
        options.add_argument("--enable-javascript")
        options.binary_location = '/usr/bin/brave-browser'
        driver = webdriver.Chrome(options=options, executable_path='/usr/local/bin/chromedriver')
    else: 
        options = webdriver.ChromeOptions()
        options.add_argument("--enable-javascript")
        driver = webdriver.Chrome(options=options)
    
    with open('sites.csv', 'r') as arqcsv:
        reader = csv.reader(arqcsv, delimiter = ',')
        rows = list(reader)
        linkslist = rows[0]
        visitedlist = []
        for k in linkslist:
            count = 0
            sitelinks = []
            sitelinksaux = []
            sitelinks.append((k,1))
            sitelinksaux.append(k)
            while (count < 1000 and len(sitelinks) > count):  
                aux = sitelinks.pop(0)[0]
                driver.get(aux)
                for f in range(randint(3, 13)):
                    if f%2 == 1:
                        driver.execute_script("if(document.body.scrollHeight) { window.scrollTo(0,(document.body.scrollHeight/"+str(f)+")) }")                        
                        sleep(0.4)
                    else:
                        driver.execute_script("if(document.body.scrollHeight) { window.scrollTo(0,(document.body.scrollHeight/"+str(f)+")) }")
                        sleep(0.6)
                page = driver.page_source
                if not exists('./minerados/db/{}.html'.format(count+1000*(linkslist.index(k)))):
                    with open('./minerados/db/{}.html'.format(count+1000*(linkslist.index(k))), 'w') as arqhtml:
                        arqhtml.write(page)
                        arqhtml.close()
                soup = BeautifulSoup(page, 'html.parser')
                heu = filtroGuiado(soup)
                for pondlink in heu:
                    strlink = pondlink[0]
                    if(not strlink == None):
                        #check and correct //
                        if strlink[0:2] == "//" :
                            strlink = strlink[2:]
                        #start with / or contain "home - http"
                        if (strlink[0:1] == "/"):
                            strlink = k + strlink
                        if (strlink[0:3] == "www"):
                            strlink = "https://" + strlink
                        #loop handler
                        if (k == "https://www.amazon.com.br"):
                            strlink = strlink.split("ref")[0]
                        if (k == "https://www.mercadolivre.com.br"):
                            strlink = strlink.split("#")[0]
                        if (k == "https://www.magazineluiza.com.br"):
                            strlink = strlink.split("url")[len(strlink.split("url"))-1]    
                        if filter(strlink, k, robotstxt[k]["disallow"] ):
                            if strlink not in sitelinksaux:
                                if strlink[0:5] == "https":
                                    aux = pondlink[1]
                                    sitelinks.append((strlink, aux))
                                    sitelinks = sorted(sitelinks, key=lambda x:x[1], reverse=True)
                                    sitelinksaux.append(strlink)
                count += 1  
            visitedlist.append(sitelinks)
        data = {}
        for site in visitedlist:
            data[site[0]] = site
        with open('crawlerResult.json', 'w') as outfile:
            json.dump(data, outfile) 
    return

def filter(link, root, disallowList) -> bool:
    if not regularExpression(root[12:], link):
        return False
    if not disallowCheck(link, disallowList):
        return False
    return True

def disallowCheck(link, disallowList) -> bool: 
    for disallow in disallowList:
        if regularExpression(disallow, link):
            return False
    return True

def regularExpression(expr, str) -> bool: 
    if expr[0:1] == "*":
        expr = "."+expr
    result = re.search(expr, str)
    if not result == None:
        return True
    return False    
if __name__ == "__main__":
    main()
