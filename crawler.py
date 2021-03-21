import json
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from time import sleep
import re
from json import load
from getRecDados import getBagOfWords, getTagsRem
from random import randint
from os.path import exists

def heuristica(soup):
    tags_rm = getTagsRem()
    
    for t in tags_rm:
        for element in soup.findAll(t):
            element.extract()

    return

def filtroGuiado(soup):
    a_com_link = soup.findAll('a', href=True)
    sitesAvisitar = []
    bow_estatico = getBagOfWords()
    
    for acl in a_com_link:
        for a in acl:
            try:
                k = a.find('span', href=False, recursive=True)
                if k:
                    for j in k:
                        link_a_class = ' '.join(str(j).casefold().split())
                        nota = classificador(link_a_class)
                        link_real = k.findParent('a')['href']
                        if nota > 1:
                            sitesAvisitar.insert(0, (link_real, nota))
            except Exception as e:
                # print(e)
                pass
    # print(sitesAvisitar)
    return

def main():
    cs = None
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
            sitelinks.append(k)
            while (count < 1000 or len(sitelinks)<= count):  
                driver.get(sitelinks[count])
                page = driver.page_source
                if not exists('./minerados/db/{}.html'.format(count+1000*(linkslist.index(k)))):
                    with open('./minerados/db/{}.html'.format(count+1000*(linkslist.index(k))), 'w') as arqhtml:
                        arqhtml.write(page)
                        arqhtml.close()
                soup = BeautifulSoup(page, 'html.parser')
                for link in soup.find_all('a'):
                    #check and correct //
                    strlink = link.get('href')
                    if(not strlink == None):
                        if strlink[0:2] == "//" :
                            strlink = strlink[2:]
                        #start with / or contain "home - http"
                        if (strlink[0:1] == "/"):
                            strlink = k + strlink
                        if (strlink[0:3] == "www"):
                            strlink = "https://" + strlink    
                        if filter(strlink, k, robotstxt[k]["disallow"] ):
                            if strlink not in sitelinks:
                                if strlink[0:5] == "https":
                                    sitelinks.append(strlink)
                for f in range(randint(3, 13)):
                    if f%2 == 1:
                        driver.execute_script("if(document.body.scrollHeight){ window.scrollTo(0,document.body.scrollHeight/{}) }".format(f))
                        sleep(0.6)
                    else:
                        driver.execute_script("if(document.body.scrollHeight){ window.scrollTo(0,document.body.scrollHeight/{}) }".format(f))
                        sleep(0.4)
                # sleep(12)
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
