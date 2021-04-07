import requests
from bs4 import BeautifulSoup
import pymysql
import re

#제목 텍스트 추출 함수
def clean_title(text):
    cleaned_text = re.sub('<span class="post-title" id="articleTitle" itemprop="headline">', '', text)
    cleaned_text = re.sub('</span>', '', cleaned_text)
    cleaned_text = cleaned_text.replace('[', '').replace(']', '')
    return cleaned_text

#시간 텍스트 추출 함수
def clean_time(text):
    cleaned_text = re.sub('<b>', '', text)
    cleaned_text = re.sub('</b>', '', cleaned_text)
    cleaned_text = cleaned_text.replace('[', '').replace(']', '').replace(' ', '').replace('-', '.').replace(':', '')
    cleaned_text = cleaned_text[0:-6]
    return cleaned_text

#기사내용 텍스트 추출 함수
def clean_contents(text):
    cleaned_text = re.sub('<br/>', '', text)
    cleaned_text = re.sub('<p>', '', cleaned_text)
    cleaned_text = re.sub('</p>', '', cleaned_text)
    cleaned_text = cleaned_text.replace('[', '').replace(']', '')
    cleaned_text.rstrip('\n\n')
    return cleaned_text


#db connection
conn = pymysql.connect(host='localhost', user='root', password='7898654', db='python', charset="utf8")
curs = conn.cursor()

for i in range(1, 2):
    url = f'https://www.idaegu.com/newsList/idg005000000?page={i}'
    r = requests.get(url)
    soup2 = BeautifulSoup(r.text, 'html.parser')
    news_titles = soup2.select(' article > div > h2 > a')
    for title in news_titles:
        # print(title['href'])
        href = title['href']
        print('링크 : ', href)
        if href == '':
            print('제목이 없습니다.')
        else:
            url2 = 'https://www.idaegu.com/'+href
            news_contents = requests.get(url2)
            soup = BeautifulSoup(news_contents.text, 'html.parser')
            title = soup.select('#articleTitle')
            # print("제목 : , title")
            title = str(title)
            cls1 = clean_title(title)
            print(cls1)
            time = soup.select('#content > div > div > div.col-sm-8.content-column > div.single-container > article > div > div.term-badges > div > div > span.time > time:nth-child(1) > b')
            # print(time)
            time = str(time)
            cls2 = clean_time(time)#2020. 06. 28 형식으로 출력
            print(cls2)
            cls3 = ''
            contents = soup.select('#article')
            for sa in contents:
                cls3 = sa.get_text(strip=True)
            print(cls3)
        #     news_company = "대구일보"
        #     sql = "insert into news(news_company, news_name, time, news_info) values (%s,%s,%s,%s)"
        #     curs.execute(sql, (news_company, cls1, cls2, cls3))
        #     conn.commit()
#connection 닫기.
conn.close()

