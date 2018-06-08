import random
import requests
from bs4 import BeautifulSoup
import user_agents

"""
功能: 爬取抽屉热搜榜首页资讯的标题
"""

def main():
    headers = {'User-Agent': random.choice(user_agents.agents)}
    # 请求网页信息
    resp = requests.get('https://dig.chouti.com/', headers=headers)


    # 响应编码
    # resp_encoding = resp.apparent_encoding
    # print(resp_encoding)


    # 创建一个soup对象
    soup = BeautifulSoup(resp.text, features='html.parser')
    # 找出id为content-list的标签(div)

    # 取出所有class='item'的div
    div_list = soup.find_all('div', class_='item')
    for i in div_list:
        div_news = i.find_all('div', class_='news-content')
        # 获取包含标题的div class='part2'
        div_part2 = div_news[0].find_all('div', class_='part2')
        if div_part2[0]:
            # 获取标题 share-title
            title = div_part2[0].attrs.get('share-title')
            print(title)


if __name__ == '__main__':
    main()