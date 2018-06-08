import random

import requests

from python.PythonSelf.study.chouti import user_agents

"""
功能: 使用session登录抽屉网并实现点赞功能
"""

def main():
    # 登录网站需要的参数
    data_dict = {
        'phone':'8618086869080',
        'password': 'Zz19961996',
        'oneMonth': 1
    }
    # 请求头 当网页请求不下来时,需要传入请求头
    headers = {'User-Agent': random.choice(user_agents.agents),
               'Referer': 'https://dig.chouti.com/'
               }

    # session保存访问页面时的信息 cookies headers 等
    session = requests.session()

    session.get('https://dig.chouti.com/',headers=headers)

    session.post(
        url = 'https://dig.chouti.com/login',
        data = data_dict,
        headers=headers
    )

    resp3 = session.post(
        url = 'https://dig.chouti.com/link/vote?linksId=19255556',
        headers=headers
    )
    print(resp3.text)




if __name__ == '__main__':
    main()