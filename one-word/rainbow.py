'''
彩虹屁生成器
https://chp.shadiao.app/api.php
'''
import requests

__all__ = ['get_rainbow_info']

def get_rainbow_info():

    print('获取彩虹屁信息...')
    try:
        req = requests.get('https://chp.shadiao.app/api.php')
        if req.status_code == 200:
            return req.text
        else:
            print('彩虹屁获取失败...')
    except requests.exceptions.RequestException as exception:
        print(exception)

get_one_words = get_rainbow_info

if __name__ == '__main__':
    ow = get_one_words()
    print(ow)