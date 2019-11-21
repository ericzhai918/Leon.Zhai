'''
获取one一个
'''

from bs4 import BeautifulSoup
import requests
import lxml

__all__ = ['get_wufazhuce_info']

def get_wufazhuce_info():
    pass
    print('获取 ONE 信息...')
    url = 'http://wufazhuce.com/'
    try:
        req = requests.get(url)
        if req.status_code == 200:
            soup = BeautifulSoup(req.text, 'lxml')
            one_msg = soup.find('div',class_='fp-one-cita').text
            return one_msg
        else:
            print('获取 ONE 失败。')
    except Exception as e:
        print(e)

get_one_words = get_wufazhuce_info

if __name__ == '__main__':
    ow = get_one_words()
    print(ow)