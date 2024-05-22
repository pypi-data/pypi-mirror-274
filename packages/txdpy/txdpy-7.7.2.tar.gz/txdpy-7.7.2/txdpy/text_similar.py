import requests,json
from time import sleep

params = {"grant_type": "client_credentials", "client_id": "7eb6Ee3o8FLh9ce3ATX1MA1S",
              "client_secret": "O44grcUdKtKSXXAMTkgpoDamFeweeGy7"}
access_token = str(
    requests.post("https://aip.baidubce.com/oauth/2.0/token", params=params).json().get("access_token"))

def text_similar(text_1, text_2):
    i=0
    response,e=None,None
    while i<10:
        try:
            url = "https://aip.baidubce.com/rpc/2.0/nlp/v2/simnet?charset=&access_token=" + access_token
            payload = json.dumps({
                "text_1": text_1,
                "text_2": text_2
            })
            response = requests.request("POST", url, headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
                                        data=payload).json()
            return response['score']
        except Exception as e:
            sleep(10)
            i+=1
    else:
        raise ValueError(f'相似度匹配异常：{response},{e}')