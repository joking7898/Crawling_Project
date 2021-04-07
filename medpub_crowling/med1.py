import requests
from bs4 import BeautifulSoup
import pymysql

#db connection
conn = pymysql.connect(host='localhost', user='root', password='Rlatndus3!', db='4th', charset="utf8")
curs = conn.cursor()
proxyDict = {'https': '153.126.160.91:80'}

#medpub 개수. 32940449
for i in range(15086085, 16000000):
    cls1 = ''
    cls2 = ''
    cls3 = ''
    # cls4 = ''
    # cls5 = ''
    url2 = f'https://pubmed.ncbi.nlm.nih.gov/{i}'
    print(url2)
    # proxy 설정
    news_contents = requests.get(url2, proxies=proxyDict)
    #BeautifulSoup를 사용하여 text처리를 하였습니다.
    soup = BeautifulSoup(news_contents.text, 'html.parser')
    # 논문 제목 Parsing (해당페이지에 논문이 있는지 판별.)
    title = soup.select('#full-view-heading > h1')
    for s_title in title:
        cls1 = s_title.get_text(strip=True)
    #제목이 없을경우 해당 페이지에 논문이 없기때문에 크롤링 중단.
    if cls1 == '':
        print("not found");
    else:
        # 제목 크롤링 한 결과 출력.
        print("title : ", cls1)
        # 저자 크롤링.
        name = soup.select('#full-view-heading > div.inline-authors > div > div')
        # cls2에 해당 선택한 값에 text만 가져오게 하여 선택된 name들을 반복하여
        # text만 가져오게 하는 처리를 진행한 for문입니다.
        for s_name in name:
            cls2 = s_name.get_text(strip=True)
        #저자 크롤링 출력.
        print("author : ", cls2)
        #선택된 pmid에서 text값만 가져오게하는 처리.
        PMID = soup.select('#full-view-identifiers > li:nth-child(1) > span > strong')
        for s_PMID in PMID:
            cls3 = s_PMID.get_text(strip=True)
        # pmid 출력
        print("PMID : ", cls3)
        cls4 =''
        # 연구가 수행된 기관들을 크롤링.( 관련 기관 )
        Affiliation = soup.select('#full-view-expanded-authors > div > ul > li')
        # 선택된 Affiliation 에서 text값만 가져오게하는 처리.
        for s_Affiliation in Affiliation:
            cls4 = s_Affiliation.get_text(strip=True)
        if cls4 == '':
            cls4 = 'null'
        print("Affiliation : ", cls4)
        # 논문의 abstract를 크롤링 부분. cls5는 해당 텍스트를 가져오기 위해 선언.
        cls5 = ''
        Abstract = soup.select('#enc-abstract > p')
        # 선택된 Abstract 에서 text값만 가져오게하는 처리.
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

