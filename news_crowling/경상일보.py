import requests
from bs4 import BeautifulSoup
import pymysql
import re
from requests import get

#제목 텍스트 추출 함수
def clean_title(text):
    cleaned_text = re.sub('<strong><!--CM_TITLE--><!-- s : 기사 제목 -->', '', text)
    cleaned_text = re.sub('<!-- e : 기사 제목 --><!--/CM_TITLE--></strong>', '', cleaned_text)
    cleaned_text = cleaned_text.replace('[', '').replace(']', '')
    return cleaned_text

#시간 텍스트 추출 함수
def clean_time(text):
    cleaned_text = re.sub('<div class="View_Time"><span>승인</span> ', '', text)
    cleaned_text = re.sub('</div>', '', cleaned_text)
    cleaned_text = cleaned_text.replace('[', '').replace(']', '').replace(' ', '')
    cleaned_text = cleaned_text[0:-10]
    return cleaned_text

#db connection
conn = pymysql.connect(host='localhost', user='root', password='7898654', db='python', charset="utf8")
curs = conn.cursor()

for i in range(2, 3):
    url = f'http://www.ksilbo.co.kr/news/articleList.html?page={i}&sc_section_code=S1N3&sc_sub_section_code=&sc_serial_code=&sc_area=&sc_level=&sc_article_type=&sc_view_level=&sc_sdate=&sc_edate=&sc_serial_number=&sc_word=&sc_word2=&sc_andor=&sc_order_by=I&view_type=sm'
    r = requests.get(url)
    soup2 = BeautifulSoup(r.text, 'html.parser')
    news_titles = soup2.select('td.ArtList_Title > a')
    for title in news_titles:
        # print(title['href'])
        href = title['href']
        # print('링크 : ', href)
        if href == '':
            print('제목이 없습니다.')
        else:
            url2 = 'http://www.ksilbo.co.kr/news/'+href
            print('링크 : ', url2)
            news_contents = get(url2)
            soup = BeautifulSoup(news_contents.content.decode('euc-kr', 'replace'), features="html.parser")
            title = soup.select('td:nth-child(2) > div > strong')
            # print("제목 : ", title)
            title = str(title)
            cls1 = clean_title(title)
            print(cls1)
            time = soup.select('div.View_Time')
            # print(time)#2020.06.28 형식으로 출력
            time = str(time)
            cls2 = clean_time(time)
            print(cls2)
            cls3 = ''
            contents = soup.select('#CmAdContent > p:nth-child(3)')
            for sa in contents:
                cls3 = sa.get_text(strip=True)
            if cls3 == '':
                contents = soup.select('#CmAdContent')
                for sa in contents:
                    cls3 = sa.get_text(strip=True)
            print(cls3)
            # sql = "insert into news(news_company, news_name, time, news_info) values (%s,%s,%s,%s)"
            # curs.execute(sql, ('경북일보', cls1, cls2, cls3))
            # conn.commit()
#connection 닫기.
conn.close()

