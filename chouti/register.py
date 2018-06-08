import random

import requests

from python.PythonSelf.study.chouti import user_agents

"""
功能: 登录抽屉网并实现点赞功能
"""

def main():
    # 登录网站需要的参数
    # 请求体 get没有请求体 post才有请求体
    data_dict = {
        'phone':'8618086869080',
        'password': 'Zz19961996',
        'oneMonth': 1
    }
    # 请求头/响应头 键值对
    headers = {'User-Agent': random.choice(user_agents.agents)}



    # 1. 第一次登录页面 得到第一个cookies
    resp = requests.get('https://dig.chouti.com/',headers=headers)
    resp_cookies = resp.cookies.get_dict()
    print(resp_cookies)



    # 2. 第二次请求登录 携带上一次的cookies 后台对cookies中的gpsd进行授权
    # 同时会获取到一个与第一次不相同的cookies值
    resp1 = requests.post(
        url = 'https://dig.chouti.com/login',
        data = data_dict,
        headers = headers,
        cookies = resp_cookies
    )
    # resp1.text返回str类型
    # {"result":{"code":"9999", "message":"", "data":{"complateReg":"0","destJid":"cdu_52457367115"}}}  code":"9999"表示登录成功
    # resp1.cookies.get_dict() f返回字典类型的cokkies
    # {'puid': '5a38e5e265bcb6fe3450ebed6bf4d6de', 'gpid': '921f4f2c9f3344af8a815fecaf88af83', 'route': '340ad5ec7bdbaaaa2d4d12be04eae5d2'}



    # 3. 登录成功 传入第一次获取的cookies里面的'gpsd'的值  实现点赞功能
    resp2 = requests.post(
        url = 'https://dig.chouti.com/link/vote?linksId=19255556',
        cookies = {'gpsd':resp_cookies.get('gpsd')},
        headers = headers
    )
    print(resp2.text)
    # resp2.text 返回推荐(点赞)成功信息
    # {"result":{"code":"9999", "message":"推荐成功", "data":{"jid":"cdu_52457367115","likedTime":"1524668996922000","lvCount":"9","nick":"萍姐姐","uvCount":"2","voteTime":"小于1分钟前"}}}




if __name__ == '__main__':
    main()