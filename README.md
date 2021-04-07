# Crawling_Project
- python, Beautiful Soup를 사용하여 pubmed 와 각 지역 신문사를 크롤링 하였습니다.
# 1. PUBMED 크롤링

의학용 논문 데이터셋 구축하기 위해 크롤링을 하였습니다.

## pubmed 란?
![medpub](https://user-images.githubusercontent.com/39583653/113894585-1e8fda80-9803-11eb-9153-75d6b2202bd4.png)

펍메드(영어: PubMed)는 생명과학 및 생물의학 그리고 건강심리학등 보건 및 복지에 관한 폭넓은 주제에 대한 참조 및 요약을 담고 있는 MEDLINE 데이터베이스를 주로 접근할 수 있게 해 주는 자유 검색 엔진이다

사용언어는 **python**이며 **BeautifulSoup**를 사용하여 크롤링 하였습니다.

ps. **proxy**를 잠시 사용한 버전입니다. (44만개를 여러개의 py 파일을 실행하여 병렬적으로 크롤링을 진행하다가 bot의 공격으로 오인하여 ip를 영구 정지당하였습니다.)

- 해당 크롤러의 저장소인 데이터베이스의 형태입니다.

![Untitled](https://user-images.githubusercontent.com/39583653/113895038-85ad8f00-9803-11eb-9a00-a15f94af2c42.png)

pubmed의 pmid(고유 id값)에 모든 내용이 없는것을 확인하고 해당 pmid에 논문의 내용이 있는지 없는지에 대한 판별은 제목의 유무로 판단하였습니다.

- 소스코드

```python
import requests
from bs4 import BeautifulSoup
import pymysql

#db connection
conn = pymysql.connect(host='localhost', user='root', password='xxxx', db='4th', charset="utf8")
curs = conn.cursor()
proxyDict = {'https': '153.126.160.91:80'}

#medpub 개수. 32940449
for i in range(15086085, 16000000):
    cls1 = ''
    cls2 = ''
    cls3 = ''
    cls4 = ''
    cls5 = ''
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
```

해당 작업을 연속적으로 하게 되어 결과는 아래의 db로 즉각적으로 입력되어있습니다. 

![dbresults](https://user-images.githubusercontent.com/39583653/113895028-8514f880-9803-11eb-8028-d412b2b26ef5.png)

해당 작업의 결과물이며 해당작업의 링크도 옆에 동일하게 설정하였습니다.

해당 크롤러로 병렬적으로 여러 프로세스를 틀어서  44만개 정도의 데이터를 축적하였습니다.

![count_db](https://user-images.githubusercontent.com/39583653/113895022-83e3cb80-9803-11eb-985c-c56774cb43f0.png)

# 2. 지역신문사 기사 크롤링

2020 시공간인공지능 1년차 자료구축 크롤러입니다. 

![rodemap](https://user-images.githubusercontent.com/39583653/113895034-8514f880-9803-11eb-9af7-4a4f674d6d69.png)

대학교 연구실로 1차년도에 해당하는 데이터를 수집하는 과정에서 작성한 크롤러 입니다.

각 지역지의 신문들의 사회 일반, 환경 및 보건복지 부분에 대한 해당지역의 사건에 대한 정보를 수집하기 위해서 기사들을 수집하였습니다.

대표적 함수

clean_title(text) - 소스코드를 제외한 실제 기사의 제목만을 추출.

clean_time(text) - 소스코드를 제외한 실제 기사의 시간을 추출.

clean_contents(text) - 소스코드를 제외한 실제 기사의 내용만을 추출.

모두 위의 함수들은 python의 re 모듈을 사용하여 추출하였습니다.

- 현재 작성한 크롤러 (27개 신문사)
    - 강원일보
    - 강원도민일보
    - 경남일보
    - 경남도민일보
    - 경남매일
    - 경기일보
    - 경북도민일보
    - 경북매일신문
    - 경북신문
    - 경북신문
    - 경북일보
    - 경상일보
    - 경인일보
    - 고양신문
    - 광남일보
    - 광주매일신문
    - 국제신문
    - 굿모닝충청
    - 금강일보
    - 김해뉴스
    - 남도일보
    - 뉴스경남
    - 당진신문
    - 대구일보
    - 대전일보
    - 대전시티저널
    - 대전투데이
