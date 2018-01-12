# -*- coding: utf-8 -*-
# import sys
import os
import collections
import re

# sys.path.append("/mnt/home/appuser/cbpython/tools/tool.py")
# path = 'C:\\Users\\cb\Downloads\\2\\'
path = '/mnt/home/appuser/chat_data201712/'


# 根据规则读取日志文件，提取所需要的内容，写入新的文件
def get_content(file_name):
    list_1 = list()
    for line in open(file_name, "r"):
        try:
            line = line.strip("\n")
            item_list = line.split("\t")
            if item_list[3] == "2300102" and item_list[4] == "30":
                list_1.append(line)
        except Exception as e:
            print(str(e))

    str_file = "\n".join(list_1)
    f = open(path + 'extract_data.txt', "a")
    f.write(str_file)
    f.close()


# 读取待处理的内容，统计频次
def frequency_record():
    list_1 = []
    for line in open(path + "extract_data.txt", "r"):
        try:
            list_1.append(line.strip("\n"))
        except Exception as e:
            print(e)
    # 统计频次，并排序
    list_new = Tool.frequency_calculate(list_1)
    # #写入文件
    list_file = []
    for i in list_new:
        list_file.append("\t".join(map(str, i)))
    str_file = "\n".join(list_file)
    str_file += "\n"

    f = open(path + "statistics_result.txt", "a")
    f.write(str_file)
    f.close()

    os.remove(path + "extract_data.txt")


# 按天统计过的数据，存在重复情况，合并相同问题的频次
def combine_frequency():
    dict1 = dict()
    for line in open(path + "statistics_result.txt", "r"):
        try:
            item = line.strip("\n")
            item_list = item.split("\t")

            item_words = item_list[0].strip("|")
            item_value = int(item_list[1])

            value = dict1.get(item_words)
            if value:
                value += item_value
                dict1[item_words] = value
            else:
                dict1[item_words] = int(item_value)
        except Exception as e:
            print("error", repr(e))
    print(dict1.__len__())

    f = open(path + "combin_result.txt", "a")
    for key, value in dict1.items():
        content = key + "\t" + str(value) + "\n"
        f.write(content)
    f.close()


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

    # 判断字符串是否包含汉字
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
        for line in open(file_path + file_name, "r"):
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

        f = open(file_path + "sort_result.txt", "a")
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


if __name__ == '__main__':
    # 读取所有log文件路径
    logs = Tool.get_all_files(path)
    for log in logs:
        print(log)
        # print("processing......")
        # 根据规则提取原始日志文件
        get_content(log)
        # 单个文件频次统计
        # frequency_record()
    # 频次合并
    # combine_frequency()
    # 排序
    # Tool.sort_repeat(path, "combin_result.txt")
