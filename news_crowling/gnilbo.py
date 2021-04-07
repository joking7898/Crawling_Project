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
    url = f'http://www.gnnews.co.kr/news/articleList.html?page={i}&box_idxno=&sc_sub_section_code=S2N4&view_type=sm'
    r = requests.get(url)
    soup2 = BeautifulSoup(r.text, 'html.parser')
    news_titles = soup2.select(f'div.list-titles > a')
    # print(news_titles)
    for title in news_titles:
        href = title['href']
        # print(href)
        if href == '':
            print('제목이 없습니다.')
        else:
            url2 = 'http://www.gnnews.co.kr'+href
            news_contents = requests.get(url2)
            soup = BeautifulSoup(news_contents.text, 'html.parser')
            title = soup.select('#user-container > div.float-center.max-width-960 > header > div > div')
            title = str(title)
            cls1 = clean_title(title)
            # print(cls1)
            time = soup.select('#user-container > div.float-center.max-width-960 > header > section > div > ul > li:nth-child(2)')
            time = str(time)
            cls2 = clean_time(time)
            contents = soup.select('#article-view-content-div > div.news_content > div > font')
            # contents = str(contents)
            cls3 = ''
            for sa in contents:
                cls3 = sa.get_text(strip=True)
            #기사 내용 크롤링 방식 다를때.
            if cls3 == '':
                contents = soup.select('#article-view-content-div')
                for sa in contents:
                    cls3 = sa.get_text(strip=True)
            # cls3 = clean_contents(contents)
            news_company = "경남일보"
        #     print(cls1)
        #     print(cls2)
        #     print(cls3)
            sql = "insert into news(news_company, news_name, time, news_info) values (%s,%s,%s,%s)"
            curs.execute(sql, (news_company, cls1, cls2, cls3))
            conn.commit()
#connection 닫기.
conn.close()