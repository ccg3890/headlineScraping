from urllib import request
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

#html
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
results = []
contents = []
pages = []
okt = Okt()

processing_start_time = str((datetime.datetime.now()).strftime('%Y%m%d%H%M'))
print("===============processing_start_time")
print(processing_start_time)

#뉴스
domain = "https://www.zooseyo.or.kr";

imgcount=0
for pageNum in range(400):
    response = requests.get(domain+"/Yu_board/petcare.html?area=&animal=강아지&page="+str(pageNum).strip(),headers=headers, timeout=10)
    bs = BeautifulSoup(response.content, "html.parser")
    rowindex = 0
    for row in bs.select(" a > img"):
        if(str(row.attrs['src']).find("care") > 0) :
            try:
                imgUrl = domain+str(row.attrs['src']).replace("..","")
                filename = imgUrl.split("/")[5]
                print("pageNum=",pageNum,"imgcount=",imgcount,"url=",imgUrl)
                request.urlretrieve(imgUrl,base_dir+"dog/"+filename)

                lv1 = bs.select(" a > img")[rowindex].parent.parent.parent.contents[3].get_text().strip()# 동물종류
                lv2 = bs.select(" a > img")[rowindex].parent.parent.parent.contents[5].get_text().strip()# 상세설명
                lv3 = bs.select(" a > img")[rowindex].parent.parent.parent.contents[7].get_text().strip()# 발견장소
                lv4 = bs.select(" a > img")[rowindex].parent.parent.parent.contents[9].get_text().strip()# 일자
                lv5 = bs.select(" a > img")[rowindex].parent.parent.parent.contents[11].get_text().strip()# 조회수
                # print(imgUrl)
            except:
                print("pageNum=",pageNum,"imgcount=",imgcount,"url=",imgUrl)

        rowindex+=1
        imgcount+=1

processing_end_time = str((datetime.datetime.now()).strftime('%Y%m%d%H%M'))
print("===============processing_end_time")
print(processing_end_time)

# df = pd.DataFrame(results, columns=['일자','신문사','제목','요약','Link url'])
#
# file_generation_time = str((datetime.datetime.now()).strftime('%Y%m%d%H%M'))
#
#
# file_nm = "Azuki정리.xlsx"
# xlxs_dir = os.path.join(base_dir, file_nm)
#
# df.to_excel(xlxs_dir,
#             sheet_name = 'Azuki정리',
#             float_format = "%.2f",
#             header = True,
#             #columns = ["group", "value_1", "value_2"], # if header is False
#             index = True,
#             index_label = '번호',
#             startrow = 0,
#             startcol = 0,
#             #engine = 'xlsxwriter',
#             )