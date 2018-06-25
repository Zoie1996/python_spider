import re

from get_html import get_html


def get_title(result_html):
    title_url_list = re.findall('<li><a href="(.*?)" title=.*?target="_blank">(.*?)</a></li>', result_html)
    return title_url_list


def get_content(title_url_list):
    with open('格言.txt', 'a', encoding='utf-8') as f:
        for title in title_url_list[:5]:
            url = 'https://www.geyanw.com%s' % title[0]
            content_html = get_html(url)
            content_list = re.findall('<p>(.*?)</p>', content_html)
            f.write('\n\n'+str(title[1])+'\n\n')
            for content in content_list:
                f.write(str(content).replace('&nbsp;','')+'\n')



def main():
    url = 'https://www.geyanw.com/'
    result_html = get_html(url)
    title_url_list = get_title(result_html)
    # get_title(result_html)
    get_content(title_url_list)


if __name__ == '__main__':
    main()
