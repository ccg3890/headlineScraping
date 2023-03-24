import requests
import datetime
from konlpy.tag import Okt
from bs4 import BeautifulSoup
import os
import pandas as pd

starting_time = str((datetime.datetime.now()).strftime('%Y%m%d%H%M'))

print("===============string_time")
print(starting_time)

base_dir = "D:/"

#헤드라인 추출
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
results = []
contents = []
pages = []
okt = Okt()
word_counter = ['azuki']

print(word_counter)

# 헤드라인 기준 상위 30개 상세 추출
detail_searching = ""


processing_start_time = str((datetime.datetime.now()).strftime('%Y%m%d%H%M'))
print("===============processing_start_time")
print(processing_start_time)

#뉴스
response = requests.get("https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query=azuki&oquery=azuki&tqi=itwp8lp0JXVssOISlyCssssssMN-426107&nso=so%3Ar%2Cp%3Afrom20200101to20230323&de=2023.03.23&ds=2020.01.01&mynews=0&office_section_code=0&office_type=0&pd=3&photo=0&sort=0".strip(),headers=headers, timeout=10)
# 통합
# response = requests.get("https://search.naver.com/search.naver?where=view&query=azuki&sm=tab_opt&nso=so%3Ar%2Cp%3A1y%2Ca%3Aall&mode=normal&main_q=&st_coll=&topic_r_cat=".strip(),headers=headers, timeout=10)
bs = BeautifulSoup(response.content, "html.parser")

for x in bs.select(".sc_page_inner > a"):
    if x:
        url = 'https://search.naver.com/search.naver'+x.attrs['href']
        response = requests.get(url.strip(),headers=headers, timeout=10)
        xs = BeautifulSoup(response.content, "html.parser")
        for n in xs.select(".news_area"):
            if n:
                date = n.select("span.info")[0].contents[0]
                thumb = n.select("a.info")[0].contents[1]
                title = n.select(".news_tit")[0].attrs['title']
                content = ''.join(str(y) for y in n.select(".dsc_wrap a")[0].contents)
                url = n.select(".news_dsc > div > a")[0].attrs['href']
                # print(date +"|"+thumb+"|"+title+"|"+content+"|"+url)
                reponse = requests.get(url.strip(),headers=headers, timeout=10)
                sb = BeautifulSoup(response.content, "html.parser")
                results.append([date,thumb,title,content,url])

processing_end_time = str((datetime.datetime.now()).strftime('%Y%m%d%H%M'))
print("===============processing_end_time")
print(processing_end_time)

df = pd.DataFrame(results, columns=['일자','신문사','제목','요약','Link url'])

file_generation_time = str((datetime.datetime.now()).strftime('%Y%m%d%H%M'))


file_nm = "Azuki정리.xlsx"
xlxs_dir = os.path.join(base_dir, file_nm)

df.to_excel(xlxs_dir,
            sheet_name = 'Azuki정리',
            float_format = "%.2f",
            header = True,
            #columns = ["group", "value_1", "value_2"], # if header is False
            index = True,
            index_label = '번호',
            startrow = 0,
            startcol = 0,
            #engine = 'xlsxwriter',
            )