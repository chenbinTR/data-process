# -*- coding: utf-8 -*-
from tools.tool import *

path = 'C:\\Users\\cb\\Downloads\\data201710\\'


# 根据规则读取日志文件，提取所需要的内容，写入新的文件
def get_content(file_name):
    list_1 = list()
    for line in open(file_name, "r", encoding="UTF-8"):
        try:
            item_list = line.split("\t")
            # if ("2300102" == item_list[1] and item_list[2].strip("\n") in ["2", "14", "15", "17", "19", "22",
            #                                                                "50"]):
            if item_list[1] in ("2300101", "2300102", "2300103"):
                # que = item_list[0].strip()
                # if que.__len__() <= 20:
                type = item_list[1]+"-"+item_list[2].strip("\n")
                list_1.append(type)
        except Exception as e:
            print(str(e))
            print("当前行： " + line)

    str_file = "\n".join(list_1)
    f = open(path + 'extract_data.txt', "a", encoding="UTF-8")
    f.write(str_file)
    f.close()


# 读取待处理的内容，统计频次
def frequency_record():
    list_1 = []
    for line in open(path + "extract_data.txt", "r", encoding="UTF-8"):
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

    f = open(path + "statistics_result.txt", "a", encoding="UTF-8")
    f.write(str_file)
    f.close()

    os.remove(path + "extract_data.txt")


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
    # 读取所有log文件路径
    logs = Tool.get_all_files(path)
    for log in logs:
        print(log)
        print("processing......")
        # 根据规则提取原始日志文件
        # get_content(log)
        # 单个文件频次统计
        # frequency_record()
    # 频次合并
    combine_frequency()
