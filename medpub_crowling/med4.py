import requests
from bs4 import BeautifulSoup
import pymysql

#db connection
conn = pymysql.connect(host='localhost', user='root', password='Rlatndus3!', db='4th', charset="utf8")
curs = conn.cursor()
proxyDict = {'https': '140.227.80.230:3218'}

#medpub 개수. 32940449
for i in range(18048029, 19000000):
    cls1 = ''
    cls2 = ''
    cls3 = ''
    cls4 = ''
    cls5 = ''
    url2 = f'https://pubmed.ncbi.nlm.nih.gov/{i}'
    print(url2)
    news_contents = requests.get(url2, proxies=proxyDict)
    soup = BeautifulSoup(news_contents.text, 'html.parser')
    title = soup.select('#full-view-heading > h1')
    for s_title in title:
        cls1 = s_title.get_text(strip=True)
    if cls1 == '':
        print("not found");
    else:
        print("title : ", cls1)
        name = soup.select('#full-view-heading > div.inline-authors > div > div')
        for s_name in name:
            cls2 = s_name.get_text(strip=True)
        print("author : ", cls2)
        PMID = soup.select('#full-view-identifiers > li:nth-child(1) > span > strong')
        for s_PMID in PMID:
            cls3 = s_PMID.get_text(strip=True)
        print("PMID : ", cls3)
        cls4 =''
        Affiliation = soup.select('#full-view-expanded-authors > div > ul > li')
        for s_Affiliation in Affiliation:
            cls4 = s_Affiliation.get_text(strip=True)
        if cls4 == '':
            cls4 = 'null'
        print("Affiliation : ", cls4)
        cls5 = ''
        Abstract = soup.select('#enc-abstract > p')
        for s_Abstract in Abstract:
            cls5 = s_Abstract.get_text(strip=True)
        print("Abstract : ", cls5)
        if cls5 == '':
            cls5 = 'null'
        sql = "insert into medpub1(pmid, title, author, Affiliation, Abstract, link) values (%s,%s,%s,%s,%s,%s)"
        curs.execute(sql, (cls3, cls1, cls2, cls4, cls5, url2))
        conn.commit()
#connection 닫기.
conn.close()

