import requests
from bs4 import BeautifulSoup

def get_content(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, features='html.parser')
    code = resp.apparent_encoding
    li_list = soup.find_all('li')
    src = []
    title = []
    for li in li_list:
        news_list = li.find('div', class_='j-r-list-c-img')
        if news_list:
            img = news_list.find('img')
            src.append(img.attrs.get('data-original'))
            title.append(img.attrs.get('title'))
    return title, src, code


def save_content(url):

    title = get_content(url)[0]
    src = get_content(url)[1]
    code = get_content(url)[2]
    with open('news.html', 'a', encoding=code) as f:
        f.write('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Title</title></head><body>')
        for i in range(len(title)):
            title_tag = '<h3>' + title[i] + '</h3>'
            img_tag = '<img src="' + src[i] + '">'
            f.write(title_tag)
            f.write(img_tag)
        f.write('</body></html>')


def main():
    url = 'http://www.budejie.com/'
    save_content(url)


if __name__ == '__main__':

    main()
