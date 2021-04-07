import string
import requests
from bs4 import BeautifulSoup
import pymysql
import re

#제목 텍스트 추출 함수
def clean_title(text):
    cleaned_text = re.sub('<h3 class="heading">', '', text)
    cleaned_text = re.sub('</h3>', '', cleaned_text)
    cleaned_text = cleaned_text.replace('[', '').replace(']', '')
    return cleaned_text

#시간 텍스트 추출 함수
def clean_time(text):
    cleaned_text = re.sub('<li><i class="icon-clock-o"></i> 입력 ', '', text)
    cleaned_text = re.sub('</li>', '', cleaned_text)
    cleaned_text = cleaned_text.replace('[', '').replace(']', '')
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
    url = f'http://www.kado.net/news/articleList.html?page={i}&sc_sub_section_code=S2N23&view_type=sm'
    r = requests.get(url)
    soup2 = BeautifulSoup(r.text, 'html.parser')
    for j in range(1, 20, 1):
        news_titles = soup2.select(f'#section-list > ul > li:nth-child({j}) > h4 > a[href]')
        #print(news_titles)
        for title in news_titles:
            href = title['href']
            # print(href)
            url2 = 'http://www.kado.net'+href
            news_contents = requests.get(url2)
            soup = BeautifulSoup(news_contents.text, 'html.parser')
            title = soup.select('#article-view > div > header > h3')
            title = str(title)
            cls1 = clean_title(title)
            time = soup.select('#article-view > div > header > div > article:nth-child(1) > ul > li:nth-child(2)')
            time = str(time)
            cls2 = clean_time(time)
            contents = soup.select('#article-view-content-div > p:nth-child(2)')
            contents = str(contents)
            cls3 = clean_contents(contents)
            news_company = "강원도민일보"
            print(cls1)
            print(cls2)
            print(cls3)
            sql = "insert into news(news_company, news_name, time, news_info) values (%s,%s,%s,%s)"
            curs.execute(sql, ('강원도민일보', cls1, cls2, cls3))
            conn.commit()
#connection 닫기.
conn.close()