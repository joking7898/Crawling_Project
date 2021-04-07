import string
import requests
from bs4 import BeautifulSoup
import pymysql
import re

#제목 텍스트 추출 함수
def clean_title(text):
    cleaned_text = re.sub('<div class="article-head-title">', '', text)
    cleaned_text = re.sub('</div>', '', cleaned_text)
    cleaned_text = cleaned_text.replace('[', '').replace(']', '')
    return cleaned_text

#시간 텍스트 추출 함수
def clean_time(text):
    cleaned_text = re.sub('<li><i class="fa fa-clock-o fa-fw"></i> 승인 ', '', text)
    cleaned_text = re.sub('</li>', '', cleaned_text)
    cleaned_text = cleaned_text.replace('[', '').replace(']', '')
    cleaned_text = cleaned_text[0:-5]
    return cleaned_text

#db connection
conn = pymysql.connect(host='localhost', user='root', password='7898654', db='python', charset="utf8")
curs = conn.cursor()

for i in range(1, 2):
    url = f'http://www.gndomin.com/news/articleList.html?page={i}&box_idxno=&sc_sub_section_code=S2N3&view_type=sm'
    r = requests.get(url)
    soup2 = BeautifulSoup(r.text, 'html.parser')
    for j in range(1, 20, 1):
        news_titles = soup2.select(f'#user-container > div.float-center.max-width-1080 > div.user-content > section > article > div.article-list > section > div:nth-child({j}) > div.list-titles > a')
        # print(news_titles)
        for title in news_titles:
            href = title['href']
            url2 = 'http://www.gndomin.com'+href
            # print(url2)
            news_contents = requests.get(url2)
            soup = BeautifulSoup(news_contents.text, 'html.parser')
            title = soup.select('#user-container > div.float-center.max-width-1080 > header > div > div')
            # print(title)
            title = str(title)
            cls1 = clean_title(title)
            # print(cls1)
            time = soup.select('#user-container > div.float-center.max-width-1080 > header > section > div > ul > li:nth-child(2)')
            time = str(time)
            cls2 = clean_time(time)
            print(cls2)
            contents = soup.select('#article-view-content-div')
            for sa in contents:
                cls3 = sa.get_text(strip=True)
            print(cls3)
            sql = "insert into news(news_company, news_name, time, news_info) values (%s,%s,%s,%s)"
            curs.execute(sql, ('경남도민일보', cls1, cls2, cls3))
            conn.commit()
#connection 닫기.
conn.close()