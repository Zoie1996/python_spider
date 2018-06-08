import requests
from bs4 import BeautifulSoup
import re


def get_content(content_url):

    resp = requests.get(content_url)
    resp.encoding = 'GB2312'
    soup = BeautifulSoup(resp.text, 'html.parser')
    contents = soup.find(class_='noveltext').text
    contents = re.sub(re.compile(r'.*?第.*?章', re.S), '', contents)
    # contents = re.sub(re.compile(r'.*?查看收藏列表', re.S), '', contents)
    contents = re.sub(re.compile(r'插入书签.*', re.S), '', contents).strip()
    contents = re.sub(r"\s{2,}", '\n\n    ', contents)
    return contents


def get_title(title_url):

    resp = requests.get(title_url)
    # 设定编码格式 此url编码为GB2312
    resp.encoding = resp.apparent_encoding
    soup = BeautifulSoup(resp.text, 'html.parser')
    # 获取书名
    name = soup.find(class_='bigtext').text
    titles = soup.find(id='oneboolt')
    tr_list = titles.find_all('tr')
    # 创建空列表用于保存 url title
    content_url = []
    title = []
    # 文章标题从第二个tr开始，18章以后为vip章节，并不能用此方法下载
    for tr in tr_list[2:21]:
        td = tr.find_all('td')
        a = td[1].find('a')
        if a:
            # 得到标题下的连接
            content_url.append(a.attrs.get('href'))
            # 得到标题
            title.append(a.text + '  ' + td[2].text.strip())
    return name, title, content_url


def save_content(title_url):
    name = get_title(title_url)[0]
    titles = get_title(title_url)[1]
    content_urls = get_title(title_url)[2]
    with open(name + '.txt', 'a+', encoding='utf-8') as f:
        f.write(name+'\n\n\n')
        for i,title in enumerate(titles):
            f.write(title + '\n\n')
            f.write(get_content(content_urls[i]) + '\n\n')


def main():

    title_url = 'http://www.jjwxc.net/onebook.php?novelid=3566484'
    save_content(title_url)


if __name__ == '__main__':

    main()