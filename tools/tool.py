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
    #判断字符串是否包含汉字
    @staticmethod
    def is_contains_chinese(data):
        p1 = "[\u4e00-\u9fa5]"
        # p1 = ".+"
        # 编译
        pattern1 = re.compile(p1)
        results = pattern1.findall(data)
        if results.__len__() == 0:
            return False
        else:
            return True


    @staticmethod
    def words_is_contains_keys(words, keys):
        list_keys = keys.split("|")
        for key in list_keys:
            if key in words:
                return key
        return None

    @staticmethod
    def sort_repeat(file_path, file_name):
        list_new = list()
        for line in open(file_path + file_name, "r", encoding="UTF-8"):
            list_temp = list()
            items = line.split("\t")
            list_temp.append(items[0])
            list_temp.append(int(items[1].strip("\n")))
            list_new.append(list_temp)
        list_new.sort(key=lambda x: x[1], reverse=True)

        # #写入文件
        list_file = []
        for i in list_new:
            list_file.append("\t".join(map(str, i)))
        str_file = "\n".join(list_file)

        f = open(file_path + "sort_result.txt", "a", encoding="UTF-8")
        f.write(str_file)
        f.close()

    @staticmethod
    def replaceAll(source_content, regex_rool, new_content):
        content = source_content
        try:
            p = re.compile(regex_rool)
            matcher = p.findall(content)
            if matcher:
                for item in matcher:
                    content = content.replace(item, new_content)
        except Exception as e:
            print(e)
        return content

