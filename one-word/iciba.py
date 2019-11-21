"""
从词霸中获取每日一句，带英文。
http://open.iciba.com/dsapi
"""
import requests
from common import (is_json)

__all__ = ['get_iciba_info']

def get_iciba_info():

    print('获取格言信息（双语）...')
    try:
        req = requests.get('http://open.iciba.com/dsapi')
        if req.status_code == 200 and is_json(req):
            content_dict =  req.json()
            content = content_dict.get('content')
            note = content_dict.get('note')
            return '{}{}'.format(content,note)
        else:
            print('没有获取到格言数据。')
    except requests.exceptions.RequestException as exception:
        print(exception)

get_one_words = get_iciba_info

if __name__ == '__main__':
    ow = get_one_words()
    print(ow)



