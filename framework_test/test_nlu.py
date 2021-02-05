# -*- coding: utf-8 -*-
import json

import requests
import time

if __name__ == '__main__':
    time_start = time.time()
    test_case = ['唱个歌']
    url = "http://182.92.152.237/ds-nlu/parse"
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    count = test_case.__len__()
    exc_times = 0
    for i in range(10):
        for item in test_case:
            try:
                time.sleep(0.1)
                param_dict = {'query': item, 'apikey': '7d8335c8aff644ccb6bc52f626b95838'}
                print(param_dict)
                param = json.dumps(param_dict)
                d = requests.post(url, data=param_dict, headers=headers, timeout=0.3)
                print(json.loads(d.content))
            except Exception as e:
                exc_times += 1
                print(e)
    time_end = time.time()
    print('耗时： {} ms'.format(int((time_end - time_start) * 1000)))
