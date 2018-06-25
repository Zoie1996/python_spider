import random
import ssl
import urllib.request

import user_agents


def get_html(url):
    headers = {
        'User-Agent': random.choice(user_agents.agents),
    }
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url, headers=headers)
    res = urllib.request.urlopen(req, context=context)
    # result = res.read().decode('utf-8')
    result = res.read().decode('GBK')
    return result