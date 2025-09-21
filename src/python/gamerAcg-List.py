
#舊番抓取

import requests as rq
from bs4 import BeautifulSoup
from openpyxl import Workbook, load_workbook
import io
import time
import os
import re
import json
from datetime import datetime 

os.chdir(os.path.dirname(os.path.abspath(__file__)))#定下工作目錄位置
animeImages = "../../public/animeImages/"
oldData = "../assets/MyProject/gamerAcg-List.json"

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

def sleeptime(hour,min,sec):
    return hour*3600 + min*60 + sec

tStart = time.time()#計時開始
wb = Workbook()
title = ['中文','日文','英文','圖片','編號','上映日期','季']
allData = []

i = 1 #起始頁面
o = 30 #496 #結束頁面
index = 0

while (i<=o):#頁數
    nextlink = "https://acg.gamer.com.tw/index.php?page="+str(i)+"&p=ANIME&t=1&tnum=6225"
    nl_response = rq.get(nextlink, headers=headers) # 用 requests 的 get 方法把網頁抓下來

    print('nextlink:')
    print(nextlink)
    print('\nnl_response:')
    print(nl_response)

    soup = BeautifulSoup(nl_response.text, 'lxml') # 指定 lxml 作為解析器
    for url in soup.select('h1.ACG-maintitle a'):

        if 'class' not in url.attrs:

            print('\nurl:')
            print(url)

            response = rq.get(str('https:')+url.get('href'), headers=headers) # 用 requests 的 get 方法把網頁抓下來

            print('\nresponse:')
            print(response)

            html_doc = response.text # text 屬性就是 html 檔案
            soup = BeautifulSoup(response.text, 'lxml') # 指定 lxml 作為解析器
            if soup.select('h1') != []:
                company = soup
                # 判斷是否有H1
                if company != '' :
                    aName = soup.select('div.BH-lbox.ACG-mster_box1.hreview-aggregate.hreview h1')
                    aName1 = soup.select('div.BH-lbox.ACG-mster_box1.hreview-aggregate.hreview h2')
                    aImage = soup.select('div.BH-lbox.ACG-mster_box1.hreview-aggregate.hreview img')
                    imageURL = aImage[0].get('src')
                    aNameMix = aName + aName1
                    dateStr = soup.select('div.BH-lbox.ACG-mster_box1.hreview-aggregate.hreview ul.ACG-box1listA li')[5].text.strip()
                    match = re.search(r'\d{4}-\d{2}-\d{2}',dateStr)
                    if match:
                        date = datetime.strptime(match.group(), '%Y-%m-%d')
                        releaseDate = date.strftime('%Y年%m月%d日')
                        animeMonth = int(date.strftime("%m"))
                    else:
                        releaseDate = '未上映'

                    if 1<=animeMonth<=3:
                        season='冬季'
                    elif 4<=animeMonth<=6:
                        season='春季'
                    elif 7<=animeMonth<=9:
                        season='夏季'
                    else:
                        season='秋季'

                    print('\naName:')
                    print(aName)
                    print('\naName1:')
                    print(aName1)
                    print('\naNameMix:')
                    print(aNameMix)
                    print('\naImage:')
                    print(aImage)
                    print('\nimageURL:')
                    print(imageURL)

                    print('\nreleaseDate:')
                    print(releaseDate)
                    print('\nseason:')
                    print(season)

                    Con = ",".join([p.text.strip()  for p in aNameMix])
                    aNum = imageURL.split('/')[-1]
                    if '?' in aNum:
                        aNum = aNum.split('?')[0]
                    if not re.search(r"\d", aNum):
                        aNum = "0000000000.JPG"

                    print('\naNum')
                    print(aNum)

                    print('\nCon')
                    print(Con)

                    ConArray = Con.split(',')
                    print('\nConArray')
                    print(ConArray)

                    if not os.path.exists(animeImages):
                        os.mkdir(animeImages)
                    img = rq.get(imageURL)
                    if '?' in imageURL:
                        imageNum = str(imageURL.split('/')[-1].split('?')[0]).lower()
                    else:
                        imageNum = str(imageURL.split('/')[-1]).lower()
                    with open(animeImages + imageNum , "wb") as file:#開啟資料夾及命名圖片檔
                        file.write(img.content)#寫入圖片的二進位碼
                        index = index + 1

                    data = [
                    {
                        #'中文','日文','英文','圖片','編號','上映日期','季'
                        #'cn','jp','en','image','num','releaseDate','season'
                        'cn':ConArray[0],
                        'jp':ConArray[1],
                        'en':ConArray[2],
                        'image':aNum.lower(),
                        'num':re.findall(r"\d+",aNum)[0],
                        'releaseDate':releaseDate,
                        'season':season
                    }
                    ]
                    allData += data
                    
                print('\n--------------第'+ str(index) +'輪結束--------------')
                time.sleep(sleeptime(0,0,3))
    i = i + 1
tEnd = time.time()#計時結束

#將圖片格式統一轉換成小寫
imageFile = os.listdir(animeImages)
for fileName in imageFile:
    fileNumber , fileType = os.path.splitext(fileName)
    if fileType == ".PNG":
        newFileName = (fileNumber + ".png")
        os.chdir(animeImages)
        os.rename(fileName , newFileName)
    elif fileType == ".JPG":
        newFileName = (fileNumber + ".jpg")
        os.chdir(animeImages)
        os.rename(fileName , newFileName)

# 讀取舊資料
def parse_date(date_str):
    if date_str == '未上映':
        return datetime(1900,1,1)
    return datetime.strptime(date_str,'%Y年%m月%d日')
#儲存json
def saveJson(data):
    with io.open(oldData,"w+",encoding="utf8") as jp:
        jp.write(json.dumps(list(data),ensure_ascii=False))
try:
    if os.path.getsize(oldData)>0:
        with open(oldData,'r+',encoding='utf-8') as file:
            loadOldData = json.load(file)
        #將新資料與舊資料轉換成集合
        oldDataSet = {json.dumps(entry, ensure_ascii=False) for entry in loadOldData}
        newDataSet = {json.dumps(entry, ensure_ascii=False) for entry in allData}
        #資料合併後轉為列表
        newData = list(oldDataSet.union(newDataSet))
        #將資料依據時間排序(新→舊)
        sortedData = sorted((json.loads(entry) for entry in newData),key=lambda x:parse_date(x['releaseDate']), reverse=True)
        saveJson(sortedData)
    else:
        saveJson(allData)
        print("資料為空值，寫入抓取到的資料")
except FileNotFoundError:
    saveJson(allData)
    print("檔案不存在，寫入抓取到的資料")
print ("It cost %f sec" % (tEnd - tStart))#會自動做進位
input("按下 Enter 鍵以結束...")