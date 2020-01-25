import json
import re

import requests
from bs4 import BeautifulSoup
import os

allVideoUrl = []
allAudioUrl = []
dir = './video/'

for i in range(1, 28):
    headers = {'Host': 'www.bilibili.com',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
               'Connection': 'keep-alive',
               }

    url = "https://www.bilibili.com/video/av79827258/?p={}".format(i)
    html = requests.get(url=url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")
    pattern = re.compile(r'"backup_url"')
    script = soup.find("script", text=pattern).text.split('window.__playinfo__=')[1]
    jsonData = json.loads(script)
    videoBaseUrl = jsonData['data']['dash']['video'][0]['baseUrl']
    audioBaseUrl = jsonData['data']['dash']['audio'][0]['baseUrl']

    allVideoUrl.append(videoBaseUrl)
    allAudioUrl.append(audioBaseUrl)

print(allVideoUrl)
print(len(allVideoUrl))
print(allAudioUrl)
print(len(allAudioUrl))

https_headers = {
    'Origin': 'https://www.bilibili.com',
    'Referer': 'https://www.bilibili.com/video/av79827258/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}

for i in range(20, 28):
    # 下载视频
    videoName = 'temp-video-{}'.format(i)
    print("视频{}下载开始".format(videoName))
    video = requests.get(url=allVideoUrl[i - 1], headers=https_headers).content
    with open('./video/' + videoName + '.mp4', 'wb+') as f:
        f.write(video)
    print("视频{}下载结束".format(videoName))

    # 下载音频
    audioName = 'temp-audio-{}'.format(i)
    print("音频{}下载开始".format(audioName))
    audio = requests.get(url=allAudioUrl[i - 1], headers=https_headers).content
    with open('./video/' + audioName + '.mp4', 'wb+') as f:
        f.write(audio)
    print("音频{}下载结束".format(audioName))

    print("合并开始:{}和{}".format(videoName, audioName))
    finalName = 'CS229-{}'.format(i)
    ss = 'cd %s && ffmpeg -i %s.mp4 -i %s.mp4 -c copy %s.mp4' % (dir, videoName, audioName, finalName)
    os.system(ss)
    print("合并结束：%s" % finalName)
# https://zhuanlan.zhihu.com/p/96538085
