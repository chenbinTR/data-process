# -*- coding: utf-8 -*-
import json

import requests
import time
import re

if __name__ == '__main__':
    result = list()
    count = 0
    count1 = 0
    for line in open("C:\\Users\\cb\\Desktop\\fsdownload\\shinaide01.txt", "r", encoding="UTF-8"):
        count1+=1
        if line is None:
            continue
        line = int(line.strip("\n"))
        if line > 50:
            print(line)
            count += 1
        # if "request_time=" not in line:
        #     continue
        # items = line.split("request_time=")
        # result.append(items[1].replace("ms",""))
    # content = "\n".join(result)
    # f = open("C:\\Users\\cb\\Desktop\\fsdownload\\shinaide01.txt", "a", encoding="UTF-8")
    # f.write(content)
    # f.close()
    print(count1)
    print(count)
    print(count/count1)

