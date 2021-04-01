#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding: utf-8

"""
@author ChenOT
@desc
@date 2021/2/24
"""
import json
import re
from pypinyin import pinyin

if __name__ == "__main__":
    f1 = open('E:\\ci_pinyin.txt', "a", encoding="UTF-8")
    with open('E:\\ci.txt', encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.__len__() < 2:
                continue
            pinyin_re = pinyin(line)
            if line.__len__() != pinyin_re.__len__():
                print(line)
                continue
            pinyin_str = []
            for item in pinyin_re:
                pinyin_str.append("".join(item).strip())

            if pinyin_str.__len__() != line.__len__():
                print(line)
                continue

            f1.write(line + '\t' + ' '.join(pinyin_str) + '\n')
    f1.close()
