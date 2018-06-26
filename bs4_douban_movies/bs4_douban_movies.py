import random
from urllib import parse

import requests

import user_agents

def get_response(url):
    """
    第一步
    :param url: 查询的链接
    获取网页响应信息
    """
    headers = {
        'User-Agent': random.choice(user_agents.agents),
        'Referer': 'https://movie.douban.com/'
    }
    resp = requests.get(url, headers=headers)
    # resp.json() 返回ajax加载的json数据
    return resp.json()


def get_tags(url):
    """
    第二步
    获取电影分类标签
    """
    resp = get_response(url)
    tags = resp['tags']
    return tags


def get_result(url, tag):
    """
    第三步
    通过分类标签获取分类下的电影名称及评分
    :param url: 请求的链接
    :param tag: 分类标签
    """
    resp = get_response(url)
    result_list = resp['subjects']
    results = ''
    for result in result_list:
        results += '%s电影: %s  评分:%s \n' % (tag, result['title'], result['rate'])
    return results


def save_result(result):
    """
    第四步
    保存信息
    :param result: 查询结果
    """
    with open('电影.txt', 'a', encoding='utf-8') as f:
        f.write(result + '\n\n')


def main():
    # 分类标签链接
    tag_url = 'https://movie.douban.com/j/search_tags?type=movie&tag=%E7%83%AD%E9%97%A8&source='
    tags = get_tags(tag_url)
    for tag in tags:
        # 通过标签组装查询的链接
        search = parse.urlencode({'tag': tag})
        result_url = 'https://movie.douban.com/j/search_subjects?type=movie&%s&sort=recommend&page_limit=20&page_start=0' % search
        results = get_result(result_url, tag)
        save_result(results)


if __name__ == '__main__':
    main()
