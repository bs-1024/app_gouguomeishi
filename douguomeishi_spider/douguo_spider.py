# -*- coding:utf-8 -*-
import requests
import json
from multiprocessing import Queue
from concurrent.futures import ThreadPoolExecutor
from save_mongo import mongo_info


class DouguoSpider(object):
    def __init__(self):
        self.headers = {
            "client": "4",
            "version": "6948.2",
            "device": "MI 6",
            "sdk": "22,5.1.1",
            "imei": "863254010682366",
            "channel": "baidu",
            # "mac": "68:EC:C5:93:30:C8",
            "resolution": "1280*720",
            "dpi": "1.5",
            # "android-id": "68ecc59330c85078",
            # "pseudo-id": "59330c8507868ecc",
            "brand": "Xiaomi",
            "scale": "1.5",
            # "timezone": "28800",
            "language": "zh",
            "cns": "3",
            "carrier": "CHINA+MOBILE",
            # "imsi": "460076823619793",
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36",
            "act-code": "910e71eff936cdd014706bf8e7f3bcc6",
            "act-timestamp": "1573542794",
            # "uuid": "9962be65-9719-4322-9622-f9ca8e5409dc",
            "battery-level": "1.00",
            "battery-state": "3",
            "newbie": "1",
            "reach": "10000",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "Keep-Alive",
            # "Cookie": "duid=61786485",
            "Host": "api.douguo.net",
            # "Content-Length": "98",
        }
        self.keyword_list = Queue()
        self.category_url = 'http://api.douguo.net/recipe/flatcatalogs'
        self.recipe_url = 'http://api.douguo.net/recipe/v2/search/0/20'
        self.pool = ThreadPoolExecutor(max_workers=20)

    def handle_index(self):
        data = {
            "client": "4",
            # "_session":"1573555230869863254010682366",
            # "v":"1573125701",
            "_vs": "2305",
        }
        resp = requests.post(url=self.category_url, headers=self.headers, data=data)
        item_dict = json.loads(resp.content.decode())
        for item1 in item_dict["result"]["cs"]:
            for item2 in item1["cs"]:
                for item3 in item2["cs"]:
                    self.keyword_list.put(item3["name"])

    def handle_caipu(self, keyword):
        data = {
            "cclient": "4",
            # "_session": "1573543230827863254010682366",
            "keyword": keyword,
            "order": "0",
            "_vs": "11102",
            "type": "0",
        }
        resp = requests.post(url=self.recipe_url, headers=self.headers, data=data)
        item_dict = json.loads(resp.content.decode())
        for item in item_dict['result']['list']:
            caipu_info = {}
            if item['type'] == 13:
                caipu_info['user_name'] = item['r']['an']
            else:
                continue
            print(caipu_info)
            mongo_info.insert_item(caipu_info)

    def run(self):
        self.handle_index()
        while self.keyword_list.qsize() > 0:
            self.pool.submit(self.handle_caipu, self.keyword_list.get())


douguo_spider = DouguoSpider()
douguo_spider.run()

















