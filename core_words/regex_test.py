# -*- coding: utf-8 -*-
from tools.tool import *
import re

if __name__ == '__main__':
    # 源文本
    key = "鹿晗是好人啊"
    # 正则表达式
    p1 = ".*?鹿晗[^！]"

    print(key.replace(p1, ""))

    # p1 = "[\u4e00-\u9fa5]"
    # p1 = ".+"
    # 编译
    pattern1 = re.compile(p1)
    print(pattern1.findall(key))
    # 查询（执行）
    matcher1 = re.search(pattern1, key)
    # 输出结果
    print(matcher1.group(0))
