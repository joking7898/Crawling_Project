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
    cleaned_text = cleaned_text.replace('[', '').replace(']', '').replace(' ', '')
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
    url = f'http://www.newsgn.com/sub.html?page={i}&section=sc4&section2='
    r = requests.get(url)
    soup2 = BeautifulSoup(r.text, 'html.parser')
    news_titles = soup2.select('#sub_read_list > div > dl > dt > a')
    for title in news_titles:
        # print(title['href'])
        href = title['href']
        print('링크 : ', href)
        if href == '':
            print('제목이 없습니다.')
        else:
            url2 = 'http://www.newsgn.com/'+href
            news_contents = requests.get(url2)
            soup = BeautifulSoup(news_contents.text, 'html.parser')
            title = soup.select('tr > td.read_title')
            print("제목 : ", title)
        #     title = str(title)
        #     cls1 = clean_title(title)
        #     print(cls1)
            time = soup.select('#contents_wrap_sub2 > table:nth-child(3) > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(3) > td > table > tbody > tr > td.text_8 > span.data2')
            print(time)
        #     time = str(time)
        #     cls2 = clean_time(time)#2020. 06. 28 형식으로 출력
        #     print(cls2)
        #     cls3 = ''
        #     contents = soup.select('#article-view-content-div')
        #     for sa in contents:
        #         cls3 = sa.get_text(strip=True)
        #     print(cls3)
        #     news_company = "금강일보"
        #     sql = "insert into news(news_company, news_name, time, news_info) values (%s,%s,%s,%s)"
        #     curs.execute(sql, (news_company, cls1, cls2, cls3))
        #     conn.commit()
#connection 닫기.
conn.close()

