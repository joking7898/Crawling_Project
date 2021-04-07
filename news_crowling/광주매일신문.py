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
    cleaned_text = re.sub('<font class="read_time">입력날짜 : ', '', text)
    cleaned_text = re.sub('</font>', '', cleaned_text)
    cleaned_text = cleaned_text.replace('[', '').replace(']', '').replace(' ', '')
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
    url = f'http://kjdaily.com/sections.php?section=5&page={i}'
    r = requests.get(url)
    soup2 = BeautifulSoup(r.content.decode('euc-kr', 'replace'), features="html.parser")
    news_titles = soup2.select('a.sublist')
    for title in news_titles:
        # print(title['href'])
        href = title['href']
        title = title.text
        print('링크 : ', href)
        if href == '':
            print('제목이 없습니다.')
        else:
            url2 = 'http://kjdaily.com/'+href
            news_contents = requests.get(url2)
            soup = BeautifulSoup(news_contents.content.decode('euc-kr', 'replace'), features="html.parser")
            cls1 = title
            print("제목 : ", cls1)
            time = soup.select('#social_top > li.right > font.read_time')
            # print(time)#2020.06.28 형식으로 출력
            time = str(time)
            cls2 = clean_time(time)
            print(cls2)
            cls3 = ''
            contents = soup.select('font.jul')
            for sa in contents:
                cls3 = sa.get_text(strip=True)
            print(cls3)
            sql = "insert into news(news_company, news_name, time, news_info) values (%s,%s,%s,%s)"
            curs.execute(sql, ('광주매일신문', cls1, cls2, cls3))
            conn.commit()
#connection 닫기.
conn.close()
