import csv
import re
from urllib import parse
from get_html import get_html


def get_job_num(html_result):
    """
    获取职位数量
    """
    result = re.findall('<em>(\d+)</em>', html_result)
    if result:
        return result


def get_city():
    """
    获取城市名称
    """
    city_html = get_html('https://www.zhaopin.com/citymap.html')
    city_list = re.findall('<strong>([\u4e00-\u9fa5]+)</strong>', city_html)
    return city_list


def get_job_info(html_result):
    # pattern = re.compile(
    #     '<td class="zwmc".*? href="(.*?)" target="_blank">(.*?)</a>.*?'  # 职位链接和职位名称
    #     '<td.*? class="fk_lv".*?<span>(.*?)</span>.*?'  # 反馈率
    #     '<td class="gsmc".*? href="(.*?)" target="_blank">(.*?)</a>.*?'  # 公司链接和公司名称
    #     '<td class="zwyx">(.*?)</td>.*?'  # 月薪
    #     '<td class="gzdd">(.*?)</td>.*?'  # 地点
    #     '<td class="gxsj".*?<span>(.*?)</span>.*?'  # 发布时间
    #     , re.S)
    # 匹配所有符合标准的内容
    # data = re.findall(pattern, html_result)

    data = re.findall('<td class="zwmc".*?href=(.*?) target="_blank">(.*?)</a>.*?'  # 职位链接和名称
                      '<td class="gsmc".*?href=(.*?) target="_blank">(.*?)</a>.*?'  # 公司链接和名称名称
                      '<td class="zwyx">(.*?)</td>.*?'  # 月薪
                      '<td class="gzdd">(.*?)</td>.*?'  # 地点
                      , html_result, re.S | re.M)

    # 去掉前面置顶的无用信息 换了职位后手动增加或者减少
    _, _, _, _, _, _, _, *items = data
    for item in items:
        job_name = item[1]
        job_name = job_name.replace('<b>', '')
        job_name = job_name.replace('</b>', '')
        yield {
            'job_name': job_name,
            'job_href': item[0],
            'company': item[3],
            'salary': item[4],
            'address': item[5],
            'company_href': item[2],
        }

# def save_job_header():


def save_job_info(file_name, rows, headers):
    with open(file_name, 'a', encoding='utf-8') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader() # 写入头部信息
        f_csv.writerows(rows)


def main(job, city):
    search = parse.urlencode({'jl': city, 'kw': job})
    url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?%s' % search
    html_result = get_html(url)
    job_info = []
    file_name = '/work/python-project/zp/python_spider/day01/' + '智联' + city + job + '.csv'
    headers = ['job_name', 'job_href', 'company', 'salary', 'address', 'company_href', ]
    for item in get_job_info(html_result):
        job_info.append(item)
    save_job_info(file_name, job_info, headers)


if __name__ == '__main__':
    job = 'python'
    city = '成都'
    main(job, city)

    # 获取各城市岗位需求
    # city_list = get_city() # 401
    # for city in city_list[:20]:
    #     search = parse.urlencode({'jl': city, 'kw': job})
    #     url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?%s' % search
    #     html_result = get_html(url)
    #     job_num_result = get_job_num(html_result)
    #     print('城市: %s 岗位: %s 需求: %s' % (city, job, job_num_result[0]))
