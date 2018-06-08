import requests
from bs4 import BeautifulSoup

"""
功能: 爬取汽车之家的相关咨询
"""

def main():

    resp = requests.get('https://www.autohome.com.cn/chengdu/')
    resp.encoding = resp.apparent_encoding
    # resp.text 获取url的字符串数据


    # 创建一个soup对象
    soup = BeautifulSoup(resp.text, features='html.parser')
    # 获得id=auto-index-lazyload-article对象
    target = soup.find(id='auto-index-lazyload-article')
    # 找到所有的li标签 返回列表
    li_list = target.find_all('li')
    for i in li_list:
        a = i.find('a') # 取出所有的a标签
        if a:
            href = a.attrs.get('href') # 获得a标签超链接

            tags = a.find('p', 'tit')
            if tags:
                txt = tags.text # 获取p标签文本内容

            img = a.find('img')
            if img:
                img_url = img.attrs.get('data-src') # 获取图片src
                temp = 'http:'+img_url
                img_name = img_url[img_url.rfind('_')+1:]
                with open('images/'+img_name, 'wb') as f:
                    f.write((requests.get(temp)).content)

            # day13 csv



if __name__ == '__main__':
    main()