# 舊番抓取

import requests as rq
from bs4 import BeautifulSoup
from openpyxl import Workbook
import io
import time
import os
import re
import json
from datetime import datetime 

# 設定工作目錄
os.chdir(os.path.dirname(os.path.abspath(__file__)))
animeImages = "../../public/animeImages/"
oldData = "../assets/MyProject/gamerAcg-List.json"

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

def sleeptime(hour, min, sec):
    return hour*3600 + min*60 + sec

tStart = time.time()
wb = Workbook()
title = ['中文','日文','英文','圖片','編號','上映日期','季']
allData = []

i = 31  # 起始頁面
o = 528 # 結束頁面
index = 0

while i <= o:
    nextlink = f"https://acg.gamer.com.tw/index.php?page={i}&p=ANIME&t=1&tnum=6225"
    nl_response = rq.get(nextlink, headers=headers)
    print(f'抓取頁面: {i} 連結: {nextlink} 狀態: {nl_response.status_code}')

    soup = BeautifulSoup(nl_response.text, 'lxml')
    for url in soup.select('h1.ACG-maintitle a'):
        if 'class' not in url.attrs:
            anime_link = 'https:' + url.get('href')
            response = rq.get(anime_link, headers=headers)
            soup_detail = BeautifulSoup(response.text, 'lxml')

            if soup_detail.select('h1') != []:
                aName = soup_detail.select('div.BH-lbox.ACG-mster_box1.hreview-aggregate.hreview h1')
                aName1 = soup_detail.select('div.BH-lbox.ACG-mster_box1.hreview-aggregate.hreview h2')
                aImage = soup_detail.select('div.BH-lbox.ACG-mster_box1.hreview-aggregate.hreview img')
                if not aImage:
                    continue

                imageURL = aImage[0].get('src')
                aNameMix = aName + aName1

                # 解析上映日期
                dateStr = soup_detail.select('div.BH-lbox.ACG-mster_box1.hreview-aggregate.hreview ul.ACG-box1listA li')[5].text.strip()
                match = re.search(r'\d{4}-\d{2}-\d{2}', dateStr)
                if match:
                    date = datetime.strptime(match.group(), '%Y-%m-%d')
                    releaseDate = date.strftime('%Y年%m月%d日')
                    animeMonth = int(date.strftime("%m"))
                else:
                    releaseDate = '未上映'
                    animeMonth = 1  # 預設冬季

                if 1 <= animeMonth <= 3:
                    season = '冬季'
                elif 4 <= animeMonth <= 6:
                    season = '春季'
                elif 7 <= animeMonth <= 9:
                    season = '夏季'
                else:
                    season = '秋季'

                Con = ",".join([p.text.strip() for p in aNameMix])
                ConArray = Con.split(',')

                # 處理圖片名稱與 num
                aNum = imageURL.split('/')[-1].split('?')[0].lower()
                if not re.search(r"\d", aNum):
                    aNum = "0000000000.jpg"

                # 建立資料
                data = {
                    'cn': ConArray[0] if len(ConArray) > 0 else '',
                    'jp': ConArray[1] if len(ConArray) > 1 else '',
                    'en': ConArray[2] if len(ConArray) > 2 else '',
                    'image': aNum,
                    'num': re.findall(r"\d+", aNum)[0] if re.search(r"\d+", aNum) else '0000000000',
                    'releaseDate': releaseDate,
                    'season': season
                }
                allData.append(data)

                # 儲存圖片
                if not os.path.exists(animeImages):
                    os.mkdir(animeImages)
                img = rq.get(imageURL)
                with open(os.path.join(animeImages, aNum), "wb") as file:
                    file.write(img.content)

                index += 1
                print(f'第 {index} 筆資料抓取完成: {data["cn"]}')
                time.sleep(sleeptime(0,0,3))
    i += 1

tEnd = time.time()

# 將圖片統一成小寫格式
for fileName in os.listdir(animeImages):
    fileNumber, fileType = os.path.splitext(fileName)
    newFileName = fileNumber.lower() + fileType.lower()
    os.rename(os.path.join(animeImages, fileName), os.path.join(animeImages, newFileName))

# 讀取舊資料
def parse_date(date_str):
    if date_str == '未上映':
        return datetime(1900,1,1)
    return datetime.strptime(date_str,'%Y年%m月%d日')

# 儲存 JSON
def saveJson(data):
    with io.open(oldData, "w+", encoding="utf8") as jp:
        jp.write(json.dumps(list(data), ensure_ascii=False))

# 合併去重
def merge_data(old_data, new_data):
    combined = {entry['num']: entry for entry in old_data}  # 先放舊資料
    for entry in new_data:
        combined[entry['num']] = entry  # 新資料覆蓋舊資料
    sorted_data = sorted(combined.values(), key=lambda x: parse_date(x['releaseDate']), reverse=True)
    return sorted_data

# 寫入 JSON
try:
    if os.path.getsize(oldData) > 0:
        with open(oldData,'r',encoding='utf-8') as file:
            loadOldData = json.load(file)
        sortedData = merge_data(loadOldData, allData)
        saveJson(sortedData)
    else:
        saveJson(allData)
        print("資料為空值，寫入抓取到的資料")
except FileNotFoundError:
    saveJson(allData)
    print("檔案不存在，寫入抓取到的資料")

print(f"It cost {tEnd - tStart:.2f} sec")
input("按下 Enter 鍵以結束...")