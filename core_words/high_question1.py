# -*- coding: utf-8 -*-
# import sys
# sys.path.append("/mnt/home/appuser/cbpython/tools/tool.py")
from tools.tool import *

path = 'E:\\'


# 根据规则读取日志文件，提取所需要的内容，写入新的文件
def get_content(file_name):
    list_0 = list()
    for line in open(path + file_name, "r", encoding="UTF-8"):
        try:
            if 'platform.chat' in line:
                list_0.append(line.strip("\n").strip())
        except Exception as e:
            print(str(e))
    print(list_0.__len__())

    str_file = "\n".join(list_0)
    f = open(path + 'extract_data.txt', "a", encoding="UTF-8")
    f.write(str_file)
    f.close()


# 读取待处理的内容，统计频次
def frequency_record():
    list_1 = []
    for line in open(path + "5.txt", "r", encoding="UTF-8"):
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

    f = open(path + "statistics_result.txt", "a", encoding="UTF-8")
    f.write(str_file)
    f.close()

# 按天统计过的数据，存在重复情况，合并相同问题的频次
def combine_frequency():
    dict1 = dict()
    for line in open(path + "statistics_result.txt", "r", encoding="UTF-8"):
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

    f = open(path + "combin_result.txt", "a", encoding="UTF-8")
    for key, value in dict1.items():
        content = key + "\t" + str(value) + "\n"
        f.write(content)
    f.close()


if __name__ == '__main__':
    # frequency_record()
    # 读取所有log文件路径
    # logs = Tool.get_all_files(path)
    # for log in logs:
    #     print(log)
    # get_content("q2_log.txt")
    frequency_record()
    # 频次合并
    # combine_frequency()
    # 排序
    # Tool.sort_repeat(path, "combin_result.txt")
