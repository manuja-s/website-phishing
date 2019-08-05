import numpy as np
from math import pi
import csv
import re
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import urllib.request
from collections import defaultdict
from random import randrange
from random import uniform

def get_domains(url):
    try:

        domain=urlparse(url).hostname
        path=urlparse(url).path
        print('path : ',path)
        if(re.search('/',path)):
            pass
        else:
            path=''    
        subdomain=urlparse(url).hostname.split('.')
        if(domain==''):
            path,domain,subdomain=-1,-1,-1
            return path,domain,subdomain
        elif(path=='' and subdomain==''):
            path,domain,subdomain=-1,1,-1
            return path,domain,subdomain
        elif(path==''):
            path,domain,subdomain=-1,1,1
            return path,domain,subdomain
        else:
            path,domain,subdomain=1,1,1
            return path,domain,subdomain
    except:
                    
        path,domain,subdomain=1,1,-1
        return path,domain,subdomain
def get_index(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
     
    try:   
        req = urllib.request.Request("https://www.google.com/search?q="+url,headers=hdr)
        html_page=urllib.request.urlopen(req)
        soup = BeautifulSoup(html_page,features="lxml")
        if("did not match any documents." in str(soup)):
            index=-1
            return index
        else:
            index=1
            return index  
        
    except:
        index=-1
        return index        


def get_rank(domain_to_query):
    
    
    try:
        url = "http://www.alexa.com/siteinfo/" + domain_to_query
        page = requests.get(url,verify=False).text
        soup = BeautifulSoup(page)
        for span in soup.find_all('span'):
            if span.has_attr("class"):
                if "globleRank" in span["class"]:
                    for strong in span.find_all("strong"):
                        if strong.has_attr("class"):
                            if "metrics-data" in strong["class"]:
                                result= strong.text
                                result=re.sub("\D", "", result)
                                
        if(result==''):
            result=-1
            return result
        else:
            
            return result 

          
    except:
        print('error found')

def out(b1,b2):

    
    w = uniform(0.0,0.9)
    w1= uniform(0,2)
    w=0.5
    w1=0
    o=(w*b1)+(w1*b2)
    
    return o
def final(o,rank):
    
    if rank >= 200000 and rank <=500000:
        e=1 / (1 + np.exp(-o))
        e=e-0.5
        return e
    if rank >= 500000:
        e=1 / (1 + np.exp(-o))
        e=e-0.6
        return e 
    if rank ==-1:
        e=1 / (1 + np.exp(-o))
        e=e-0.8
        return e    
    else:
        e=1 / (1 + np.exp(-o))
        return e   
def normalize(d1,d2):
     
    b1=d1/d1+d2
    b2=d2/d1+d2 
    
    return b1,b2    
def sigmoid(x):
    b=uniform(0.0,0.5)
    b=0.1
    l=1/(1+np.exp(-(x-b)))
    p=(float(np.exp(-(x-b))))/(float(1 + np.exp(-(x-b))))
    
    return l,p
def defuzzy(l,p):
    
    m,m1=1,1    
    r1=pi*l
    m=m*r1    
    r2=pi*p  
    m1=m*r2   
    return m,m1
 
url=input('Enter URL: ')
p,d,s=get_domains(url)
i=get_index(url)
r=get_rank(url)
inp=[url,p,d,s,i,r]
print(inp)
large=len(inp)
for each in range(1,large):
    m=float(inp[each])
    l,s1=sigmoid(m)
    d1,d2=defuzzy(l,s1)
    b1,b2=normalize(d1,d2)
    o=out(b1,b2)
    if each==5:
        rank=int(inp[each])
        e=final(o,rank)
        r=[] 
       
        if e >=0.5:
            r=[1]
        else:
            r=[-1]
        inp=inp+r  
        print(inp)
        f1=open('train.csv','a')
        csv_writer = csv.writer(f1)
        csv_writer.writerow(inp)
        f1.close()     
