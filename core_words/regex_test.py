# -*- coding: utf-8 -*-
from tools.tool import *
import re

if __name__ == '__main__':
    # 源文本
    key = "你http好13391959560http://www.baid34u.com我dfd3312232323233233是[微笑]adsb234"
    # 正则表达式
    p1 = "http[s]?://[w]{3}\.[0-9a-z]+\.com"
    # p1 = ".+"
    # 编译
    pattern1 = re.compile(p1)
    print(pattern1.findall(key))
    # 查询（执行）
    matcher1 = re.search(pattern1, key)
    # 输出结果
    print(matcher1.group(0))
