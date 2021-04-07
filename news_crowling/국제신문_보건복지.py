import requests
from bs4 import BeautifulSoup
import pymysql
import re
from requests import get

#제목 텍스트 추출 함수
def clean_title(text):
    cleaned_text = re.sub('<h1>', '', text)
    cleaned_text = re.sub('</h1>', '', cleaned_text)
    cleaned_text = cleaned_text.replace('[', '').replace(']', '')
    return cleaned_text

#시간 텍스트 추출 함수
def clean_time(text):
    cleaned_text = re.sub('<span class="f_news_date"> |  입력 : ', '', text)
    cleaned_text = re.sub('</span>', '', cleaned_text)
    cleaned_text = cleaned_text.replace('[', '').replace(']', '').replace('|', '').replace(' ', '')
    cleaned_text = cleaned_text[0:-8]
    return cleaned_text

#db connection
conn = pymysql.connect(host='localhost', user='root', password='7898654', db='python', charset="utf8")
curs = conn.cursor()

for i in range(2, 3):
    url = f'http://www.kookje.co.kr/news2011/asp/list.asp?page={i}&code=0330'
    r = requests.get(url)
    soup2 = BeautifulSoup(r.text, 'html.parser')
    news_titles = soup2.select('#tabNews_listGisa_Popular_1 > div > dl > dt > a')
    for title in news_titles:
        # print(title['href'])
        href = title['href']
        # print('링크 : ', href)
        if href == '':
            print('제목이 없습니다.')
        else:
            url2 = 'http://www.kookje.co.kr'+href
            # print('링크 : ', url2)
            news_contents = get(url2)
            soup = BeautifulSoup(news_contents.content.decode('euc-kr', 'replace'), features="html.parser")
            title = soup.select('#news_topArea > div.news_title > h1')
            # print("제목 : ", title)
            title = str(title)
            cls1 = clean_title(title)
            print(cls1)
            time = soup.select('#news_topArea > div.news_reporterDate.left > ul > li:nth-child(3) > span')
            # print(time)#2020.06.28 형식으로 출력
            time = str(time)
            cls2 = clean_time(time)
            print(cls2)
            cls3 = ''
            contents = soup.select('#news_textArea > div.news_article')
            for sa in contents:
                cls3 = sa.get_text(strip=True)
            print(cls3)
            sql = "insert into news(news_company, news_name, time, news_info) values (%s,%s,%s,%s)"
            curs.execute(sql, ('국제신문', cls1, cls2, cls3))
            conn.commit()
#connection 닫기.
conn.close()

