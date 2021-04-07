import requests
from bs4 import BeautifulSoup
from requests import get
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
    cleaned_text = cleaned_text.replace('[', '').replace(']', '').replace(' ', '').replace('시', '')
    cleaned_text = cleaned_text.replace('분', '').replace('년', '.').replace('월', '.').replace('일', '.')
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

for i in range(2, 3):
    url = f'http://www.mygoyang.com/news/articleList.html?page={i}&&sc_section_code=&sc_sub_section_code=S2N31&sc_serial_code=&sc_area=&sc_level=&sc_article_type=&sc_view_level=&sc_sdate=&sc_edate=&sc_serial_number=&sc_word=&sc_word2=&sc_andor=&sc_order_by=E&view_type=sm'
    r = requests.get(url)
    soup2 = BeautifulSoup(r.text, 'html.parser')
    news_titles = soup2.select('td.list-titles > a')
    for title in news_titles:
        # print(title['href'])
        href = title['href']
        # print('링크 : ', href)
        if href == '':
            print('제목이 없습니다.')
        else:
            url2 = 'http://www.mygoyang.com/news/'+href
            news_contents = get(url2)
            # soup = BeautifulSoup(news_contents.text, 'html.parser')
            soup = BeautifulSoup(news_contents.content.decode('euc-kr', 'replace'), features="html.parser")
            title = soup.select('#article-wrap > div.headline.border-box > font.headline-title')
            print("제목 : ", title)
            title = str(title)
            cls1 = clean_title(title)
            # print(cls1)
            time = soup.select('#head-info > div.info > ul > li.date')
            print(time)#2020.06.28 형식으로 출력
            time = str(time)
            cls2 = clean_time(time)
            # print(cls2)
            cls3 = ''
            # contents = soup.select('#articleBody > p')
            # for sa in contents:
            #     cls3 = sa.get_text(strip=True)
            # if cls3 == '':
            for j in range(2, 3):
                contents = soup.select(f'#articleBody > p:nth-child({j})')
                for sa in contents:
                    cls3 = cls3 + sa.get_text(strip=True)
            print(cls3)
            # sql = "insert into news(news_company, news_name, time, news_info) values (%s,%s,%s,%s)"
            # curs.execute(sql, ('경북일보', cls1, cls2, cls3))
            # conn.commit()
#connection 닫기.
conn.close()
