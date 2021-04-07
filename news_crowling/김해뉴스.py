import requests
from bs4 import BeautifulSoup
import pymysql
import re

#제목 텍스트 추출 함수
def clean_title(text):
    cleaned_text = re.sub('<font class="headline-title"><!--CM_TITLE-->', '', text)
    cleaned_text = re.sub('<!--/CM_TITLE--></font>', '', cleaned_text)
    cleaned_text = cleaned_text.replace('[', '').replace(']', '')
    return cleaned_text

#시간 텍스트 추출 함수
def clean_time(text):
    cleaned_text = re.sub('<li class="date">게재 ', '', text)
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

for i in range(1, 3):
    url = f'http://www.gimhaenews.co.kr/news/articleList.html?page={i}&sc_section_code=S1N1&sc_sub_section_code=S2N3&view_type=sm'
    r = requests.get(url)
    soup2 = BeautifulSoup(r.text, 'html.parser')
    news_titles = soup2.select('tr > td.list-titles > a')
    for title in news_titles:
        # print(title['href'])
        href = title['href']
        print('링크 : ', href)
        if href == '':
            print('제목이 없습니다.')
        else:
            url2 = 'http://www.gimhaenews.co.kr/news/'+href
            news_contents = requests.get(url2)
            soup = BeautifulSoup(news_contents.content.decode('euc-kr', 'replace'), features="html.parser")
            title = soup.select('font.headline-title')
            # print("제목 : ", title)
            title = str(title)
            cls1 = clean_title(title)
            print(cls1)
            time = soup.select('#head-info > div.info > ul > li:nth-child(2)')
            # print(time)
            time = str(time)
            cls2 = clean_time(time)#2020. 06. 28 형식으로 출력
            print(cls2)
            cls3 = ''
            contents = soup.select('#articleBody > p:nth-child(2)')
            for sa in contents:
                cls3 = sa.get_text(strip=True)
            if contents == '':
                contents = soup.select('#articleBody > p:nth-child(3)')
                for sa in contents:
                    cls3 = sa.get_text(strip=True)
            print(cls3)
        #     news_company = "김해뉴스"
        #     sql = "insert into news(news_company, news_name, time, news_info) values (%s,%s,%s,%s)"
        #     curs.execute(sql, (news_company, cls1, cls2, cls3))
        #     conn.commit()
#connection 닫기.
conn.close()

