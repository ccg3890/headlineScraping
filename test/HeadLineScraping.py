import requests
import pandas as pd
import os
from konlpy.tag import Okt
from collections import Counter
from time import strftime, localtime, time
from wordcloud import WordCloud
from bs4 import BeautifulSoup

starting_time = strftime('%Y%m%d%I%M%S%p',localtime(time()))

print("===============string_time")
print(starting_time)

base_dir = "D:/이슈거리들/"

#헤드라인 추출
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
response = requests.get("https://news.naver.com/main/ranking/popularDay.naver?mid=etc&sid1=111".strip(),headers=headers, timeout=10)
bs = BeautifulSoup(response.content, "html.parser")

rankingnews_box = bs.select(".rankingnews_box")
contents = []

contents_text = ""

okt = Okt()

for main_index in range(len(rankingnews_box)):

    main_title_text = rankingnews_box[main_index].select("a > span > img")[0]["alt"]

    title = rankingnews_box[main_index].select("a")

    headLine = []

    for sub_index in range(len(title)):
        try:
            obj = title[sub_index]
            if obj["class"][0] in "list_title" :
                contents_text += obj.text
                # contents.append([main_title_text,obj.text])
        except:
            print("e:"+title[sub_index])


# 워드 카운트
nouns = okt.nouns(contents_text)
words = [n for n in nouns if len(n) > 1]
# del words[30:]
word_counter = Counter(words)

print("헤드라인 추출 :")
print(word_counter)

# 헤드라인 기준 상위 30개 상세 추출
detail_searching = ""


processing_start_time = strftime('%Y%m%d%I%M%S%p',localtime(time()))
print("===============processing_start_time")
print(processing_start_time)

for key_word in word_counter:
    response = requests.get("https://search.naver.com/search.naver?where=news&query="+key_word.strip()+"&sm=tab_opt&sort=1&photo=0&field=0&pd=7&ds=2022.11.21.10.11&de=2022.11.22.11.11&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Add%2Cp%3Aall&is_sug_officeid=0",headers=headers, timeout=10)
    bs = BeautifulSoup(response.content, "html.parser")
    for n in bs.select(".news_tit"):
        if n:
            detail_searching += n.text
            contents.append([key_word,n.text])

processing_end_time = strftime('%Y%m%d%I%M%S%p',localtime(time()))
print("===============processing_end_time")
print(processing_end_time)


nouns = okt.nouns(detail_searching)
words = [n for n in nouns if len(n) > 1]
word_counter = Counter(words)

print("상세 추출 :")
print(word_counter)


# 워드 클라우드 2차
wc = WordCloud(font_path='malgun', width=400, height=400, scale=2.0, max_font_size=250)
gen = wc.generate_from_frequencies(word_counter)
wc.to_file(base_dir+'상세 추출.png')




df = pd.DataFrame(contents, columns=['신문사','이슈거리들'])

this_time = strftime('%Y%m%d%I%M%S%p',localtime(time()))


file_nm = "이슈거리들"+this_time+".xlsx"
xlxs_dir = os.path.join(base_dir, file_nm)

df.to_excel(xlxs_dir,
            sheet_name = 'Sheet1',
            float_format = "%.2f",
            header = True,
            #columns = ["group", "value_1", "value_2"], # if header is False
            index = True,
            index_label = 'rownum',
            startrow = 0,
            startcol = 0,
            #engine = 'xlsxwriter',
            )

