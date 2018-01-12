# -*- coding: utf-8 -*-
from tools.tool import *

path = 'C:\\Users\\cb\\Downloads\\aofei\\'


# 读取待处理的内容，统计频次
def get_answer_by_question():
    dict_origin = dict()
    print("开始读取origin")
    for line in open(path + "sort_result.txt", "r", encoding="UTF-8"):
        try:
            items = line.split("\t")
            que = items[0]
            count = int(items[1].strip("\n"))

            # if count >=:
            dict_origin[que] = count
        except Exception as e:
            print(line)
            print(e)
    # 统计频次，并排序
    print("开始读取result")
    list_result = list()
    for line in open(path + "aofei201010.txt", "r", encoding="UTF-8"):
        try:
            items = line.split("\t")
            que = items[0]
            answer = items[1]
            if que in dict_origin:
                temp = que + "\t" + str(dict_origin[que]) + "\t" + answer
                list_result.append(temp)
        except Exception as e:
            print(line)
            print(e)

    str_file = "\n".join(list_result)

    f = open(path + "result_1000.txt", "a", encoding="UTF-8")
    f.write(str_file)
    f.close()


def remove_repeat():
    print("开始读取origin")
    set_fiter = set()
    for line in open(path + "result_1000.txt", "r", encoding="UTF-8"):
        try:
            set_fiter.add(line.strip("\n"))
        except Exception as e:
            print(line)
            print(e)
    str_file = "\n".join(set_fiter)

    f = open(path + "result.txt", "a", encoding="UTF-8")
    f.write(str_file)
    f.close()


if __name__ == '__main__':
    # 根据统计好的高频问题，读取对应的a
    get_answer_by_question()

    # 去重
    remove_repeat()
