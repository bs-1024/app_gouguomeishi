# -*- encoding:utf-8 -*-
import requests

url = 'http://ip.hahado.cn/ip'
proxies = {
    'http': 'http://H211EATS905745KC:F8FFBC929EB7D5A7@http-cla.abuyun.com:9030'
}
resp = requests.get(url=url, proxies=proxies)
print(resp.text)
