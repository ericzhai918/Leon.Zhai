import json
import re

import requests
from bs4 import BeautifulSoup

allUrl = []

for i in range(1,28):
    headers = {'Host': 'www.bilibili.com',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
               'Connection': 'keep-alive',
               }

    url = "http://www.bilibili.com/video/av79827258/?p={}".format(i)
    html = requests.get(url=url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")
    pattern = re.compile(r'"backup_url"')
    script = soup.find("script", text=pattern).text.split('window.__playinfo__=')[1]
    jsonData = json.loads(script)
    # print(jsonData['data']['dash']['video'][0])
    baseUrl = jsonData['data']['dash']['video'][0]['baseUrl']
    # backupUrlA = jsonData['data']['dash']['video'][0]['backupUrl'][0]
    # backupUrlB = jsonData['data']['dash']['video'][0]['backupUrl'][1]
    httpsUrl = 'https:' + baseUrl.split('http:')[1]
    allUrl.append(httpsUrl)

print(allUrl)
print(len(allUrl))

for i in range(1,len(allUrl)+1):
    print('第{}集视频开始下载'.format(i))
    https_headers = {
        'Origin': 'https://www.bilibili.com',
        'Referer': 'https://www.bilibili.com/video/av79827258',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }
    video = requests.get(url=allUrl[i-1], headers=https_headers).content
    # 视频保存在与py文件同级的video文件夹下

    with open('./video/' + '{}' + '.mp4', 'wb+').format(i) as f:
        f.write(video)
