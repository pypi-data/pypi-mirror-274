from loguru import logger
from tqdm import tqdm
import requests
from lxml import etree
from .requests_operation import param_dict,headers_dict
from colorama import Fore, init
import random

init()

def get_ua():
    """Get some user-agent ,But not necessarily accepted by the website"""
    first_num = random.randint(55, 62)
    third_num = random.randint(0, 3200)
    fourth_num = random.randint(0, 140)
    os_type = [
        '(Windows NT 6.1; WOW64)',
        '(Windows NT 10.0; WOW64)',
        '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_12_6)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)
    ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                  )
    userAgent = {"user-agent":ua}
    return userAgent

def req(url:str,param=None,data=None,json=None,headers=None,verify:bool=False,zhencod=True,**kwargs):
    """
    :param url: 请求的url
    :param param: get请求参数默认为空
    :param data: post请求参数默认为空
    :param json: post请求参数默认为空
    :param headers: 默认随机User-Agent
    :param verify: 是否认证证书，默认为False
    :param tree: 是否直接返回etree.HTML()对象，默认为False
    :return: 返回reponese对象
    """
    if headers:
        if type(headers) == str:
            h=headers_dict(headers)
        else:
            h=headers
    else:
        h=get_ua()
    if param:
        res=requests.get(url,params=param_dict(param) if type(param)==str else param,headers=h,verify=verify,**kwargs)
    elif json:
        res=requests.post(url,json=param_dict(json) if type(json)==str else json,headers=h,verify=verify,**kwargs)
    elif data:
        res=requests.post(url,data=param_dict(data) if type(data)==str else data,headers=h,verify=verify,**kwargs)
    else:
        res=requests.get(url, headers=h,verify=verify,**kwargs)
    if zhencod:
        res.encoding = res.apparent_encoding
    if res.apparent_encoding=='GB2312' and data:
        data={key:bytes(value,"gbk") for key,value in data.items()}
        res = requests.post(url, data=param_dict(data) if type(data) == str else data, headers=h, verify=verify,**kwargs)
        res.encoding = res.apparent_encoding
    try:
        res.tree=etree.HTML(res.text)
    except:
        res.tree =None
    status_code=res.status_code
    if 200<=status_code<=201:
        logger.info(f'\t地址：{url}\t\t状态码：'+Fore.GREEN + str(res.status_code))
    elif status_code>=400:
        logger.info(f'\t地址：{url}\t\t状态码：' + Fore.RED + str(res.status_code))
    else:
        logger.info(f'\t地址：{url}\t\t状态码：' + Fore.YELLOW + str(res.status_code))

    return res

def dow_file(path_name,href,add_suffix=True):
    """
    :param path_name: 下载路径及文件名，c:/a.pdf
    :param href: 下载链接
    :return:
    """
    name = path_name.split('/')[-1]
    if add_suffix:
        path_name += '.'+href.split('.')[-1]
    print('开始下载：', name, href)
    res = requests.get(href, stream=True,verify=False)
    if 'Content-Length' in res.headers:
        file_size = int(res.headers.get('Content-Length'))  # 获取文件的总大小
    else:
        print('未找到文件大小标识', name, href)
        file_size=30000000
    pbar = tqdm(total=file_size)  # 设置进度条的长度
    with open(path_name, 'wb') as f:
        for chunk in res.iter_content(1024 * 1024 * 2):
            f.write(chunk)
            pbar.set_description('正在下载中......')
            pbar.update(1024 * 1024 * 2)  # 更新进度条长度
        pbar.close()
    print('下载完成：', name, href)