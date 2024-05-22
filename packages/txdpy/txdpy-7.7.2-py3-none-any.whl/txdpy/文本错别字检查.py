# -*- coding: utf-8 -*-
# @File  : 文本错别字检查.py
# @Time  : 2024/1/18 10:19
# @Author: 唐旭东
from pycorrector import Corrector
import re
from time import sleep
import requests
import json
from .read_data import ReadData


class 文本错别字检查方法一():
    """
    网上开源的代码库
    """
    def __init__(self):
        self.m = Corrector()
    def main(self,文本):
        """
        :param 文本: 要识别错别字的文本
        :return: 返回[(错误文本,可能正确的文本,错误文本出现的位置),]
        """
        return self.m.correct_batch([文本])[0]['errors'] or None

class 文本错别字检查方法二():
    """
    百度的错别字识别接口
    """
    def __init__(self):
        API_KEY,SECRET_KEY=ReadData('百度ai接口验证参数', ['API Key', 'Secret Key'],select_sql="`云api类型` = '自然语言处理'").data[-1]
        params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
        self.access_token = str(requests.post("https://aip.baidubce.com/oauth/2.0/token", params=params).json().get("access_token"))

    def main(self,文本):
        """
        :param 文本: 要识别错别字的文本
        :return: [(错误文本,可能正确的文本,错误文本出现的位置),]
        """
        url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/ecnet?charset=utf-8&access_token=" + self.access_token
        payload = json.dumps({
            "text": 文本
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload).json()
        return ([(v['ori_frag'],v['correct_frag'],v['begin_pos']) for v in response['item']['vec_fragment'] if '(' not in v['ori_frag'] and ')' not in v['ori_frag'] and v['ori_frag'] != v['correct_frag']] or None)