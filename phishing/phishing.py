from urllib.parse import urlparse
from bs4 import BeautifulSoup
import urllib.request
import re
import requests
import pandas as pd
import csv
from flask import Flask, render_template, request
from sklearn.neighbors import KNeighborsClassifier

from sklearn.model_selection import train_test_split


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/hello', methods=['POST'])
def hello():
    url = request.form['search_here']
        r=get_rank(url)
        print('Rank ',r)
        p,d,s=get_domains(url)
        print('path,domain,sub',p,d,s)
        i=get_index(url)
        print('index',i)
        inp=[r,i]
        head=["Rank","Index","Result"]
        f1=open('test.csv','w')
        csv_writer = csv.writer(f1)
        csv_writer.writerow(head)
        csv_writer.writerow(inp)
        f1.close()
    
    # train = pd.read_csv("trainn.csv")
        train = pd.read_csv("train.csv", usecols = ['Rank','Index','Result'])
        test = pd.read_csv("test.csv")
    
        x = train.drop('Result', axis=1)
        y = train['Result']
        x_test = test.drop('Result', axis=1)

        train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=.1)

        knn = KNeighborsClassifier(n_neighbors = 3)
    
        knn.fit(train_x,train_y)
        prediction=knn.predict(x_test)
  
    
        if(prediction[0]==1):
            result="Genuine Site"
        else:
            result="Phishing Site"
    
        return result



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
        print('some thing is wrong')
        return index        


def get_rank(domain_to_query):
    
    url = "http://www.alexa.com/siteinfo/" + domain_to_query
    try:

        page = requests.get(url,verify=False).text
        soup = BeautifulSoup(page)
        for div in soup.find_all('div'):
            if div.has_attr("class"):
                if "rankmini-global" in div["class"]:
                    for ndiv in div.find_all("div"):
                        if ndiv.has_attr("class"):
                            if "rankmini-rank" in ndiv["class"]:
                                result= ndiv.text
                                result=re.sub("\D", "", result)
                                
        if(result==''):
         
            result=-1
            return result
        else:
            # result=1
            return result   
    except:
        # print('error found')
        return -1    
if __name__ == '__main__':
    
    app.run(host = 'localhost', port = 3000)
    
    
