# -*- coding: utf-8 -*-

import os
import collections
import re


class Tool(object):
    # 读取制定路径下所有文件（路径）
    @staticmethod
    def get_all_files(path):
        path_dir = os.listdir(path)
        logs = list()
        for allDir in path_dir:
            log = path + allDir
            logs.append(log)
        return logs

    # 对字符串list进行去重、频次统计、并按频次倒序
    @staticmethod
    def frequency_calculate(data):
        d = collections.Counter(data)
        list_new = list()
        for k in d:
            list_temp = list()
            # 计算set中元素在原list中出现的次数
            list_temp.append(k)
            list_temp.append(d[k])
            list_new.append(list_temp)
        list_new.sort(key=lambda x: x[1], reverse=True)
        return list_new

    # 对两列数据进行排序，根据第二列的数字
    # list_data包含两列数据，中间\t隔开
    @staticmethod
    def frequency_sort(list_data):
        list_new = list()
        for line in list_data:
            list_temp = list()
            items = line.split("\t")
            list_temp.append(items[0])
            list_temp.append(int(items[1].strip("\n")))
            list_new.append(list_temp)
        list_new.sort(key=lambda x: x[1], reverse=True)
        return list_new
