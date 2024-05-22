# -*- coding: utf-8 -*-
# @File  : translate.py
# @Time  : 2023/11/14 14:36
# @Author: 唐旭东

import hashlib
import random
import requests

def translate(string):
    appid = '20220712001270949'
    q = str(string)
    secret_key = 'ODwtPobgXFes3sBML_NM'
    salt = str(random.randint(1000000000, 9999999999))
    m = hashlib.md5()
    m.update((appid + q + salt + secret_key).encode("utf8"))
    s = f'http://api.fanyi.baidu.com/api/trans/vip/translate?q={q}&from=en&to=zh&appid={appid}&salt={salt}&sign={m.hexdigest()}'
    result = requests.get(s).json()
    return result["trans_result"][0]['dst']