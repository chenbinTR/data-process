# -*- coding: utf-8 -*-
from tools.tool import *

path = 'C:\\Users\\cb\\Downloads\\3\\'


# 读取待处理的内容，统计频次
def two_file_repeat_filter():
    set_file1 = set()
    set_file2 = set()
    print("开始读取origin")
    for line in open("Q:\\产品\\中心词\\去重用.txt", "r", encoding="UTF-8"):
        try:
            set_file1.add(line.strip("\n"))
        except Exception as e:
            print(line)
            print(e)
    print(set_file1.__len__())

    for line in open(path + "all.txt", "r", encoding="UTF-8"):
        try:
            items = line.split("\t")
            que = items[0]
            if que in set_file1:
                print("重复")
                continue
            set_file2.add(line.strip("\n"))
        except Exception as e:
            print(line)
            print(e)

    str_file = "\n".join(set_file2)

    f = open(path + "result.txt", "a", encoding="UTF-8")
    f.write(str_file)
    f.close()

if __name__ == '__main__':
    two_file_repeat_filter()

