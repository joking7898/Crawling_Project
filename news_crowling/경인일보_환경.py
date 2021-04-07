import requests
from bs4 import BeautifulSoup
import pymysql
import re

#제목 텍스트 추출 함수
def clean_title(text):
    cleaned_text = re.sub('<p class="view_title">', '', text)
    cleaned_text = re.sub('</p>', '', cleaned_text)
    cleaned_text = cleaned_text.replace('[', '').replace(']', '')
    return cleaned_text

#시간 텍스트 추출 함수
def clean_time(text):
    cleaned_text = re.sub('<span class="view_date">', '', text)
    cleaned_text = re.sub('</span>', '', cleaned_text)
    cleaned_text = re.sub('발행일', '', cleaned_text)
    cleaned_text = re.sub('입력', '', cleaned_text)
    cleaned_text = cleaned_text.replace('[', '').replace(']', '').replace(' ', '').replace('-', '.').replace('제', '').replace('면', '')
    cleaned_text = cleaned_text[0:10]
    return cleaned_text


#db connection
conn = pymysql.connect(host='localhost', user='root', password='7898654', db='python', charset="utf8")
curs = conn.cursor()

for i in range(2, 3):
    url = f'http://www.kyeongin.com/main/news.php?ncid=N04_07&series=&sword=&hot=&page={i}'
    r = requests.get(url)
    soup2 = BeautifulSoup(r.text, 'html.parser')
    news_titles = soup2.select(' h2 > a')
    for title in news_titles:
        # print(title['href'])
        href = title['href']
        # print('링크 : ', href)
        if href == '':
            print('제목이 없습니다.')
        else:
            url2 = 'http://www.kyeongin.com/main/'+href
            news_contents = requests.get(url2)
            soup = BeautifulSoup(news_contents.text, 'html.parser')
            title = soup.select('#content > div:nth-child(3) > div > div.view_title_box > p.view_title')
            # print("제목 : ", title)
            title = str(title)
            cls1 = clean_title(title)
            print(cls1)
            time = soup.select('#content > div:nth-child(3) > div > div.view_title_box > span')
            # print(time)#2020.06.28 형식으로 출력
            time = str(time)
            cls2 = clean_time(time)
            print(cls2)
            cls3 = ''
            contents = soup.select('#font')
            for sa in contents:
                cls3 = sa.get_text(strip=True)
            if cls3 == '':
                contents = soup.select('#font > div > div:nth-child(2) > font')
                for sa in contents:
                    cls3 = sa.get_text(strip=True)
                if cls3 == '':
                    contents = soup.select('div.news_text > font.article')
                    for sa in contents:
                        cls3 = sa.get_text(strip=True)
            print(cls3)
            # sql = "insert into news(news_company, news_name, time, news_info) values (%s,%s,%s,%s)"
            # curs.execute(sql, ('경북일보', cls1, cls2, cls3))
            # conn.commit()
#connection 닫기.
conn.close()
