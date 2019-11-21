'''
从土味情话中获取每日一句。
https://api.lovelive.tools/api/SweetNothings
'''

import requests

__all__ = ['get_lovelive_info']

def get_lovelive_info():

    print('获取土味情话...')
    try:
        req = requests.get('https://api.lovelive.tools/api/SweetNothings')
        if req.status_code == 200:
            return req.text
        else:
            print('土味情话获取失败。')
    except requests.exceptions.RequestException as exception:
        print(exception)

get_one_words = get_lovelive_info

if __name__ == '__main__':
    ow = get_one_words()
    print(ow)
