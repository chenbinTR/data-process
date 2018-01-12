import re
from tools.tool import *

list_result = list()


def frequency_record():
    list_1 = []
    for line in open("C:\\Users\\cb\\Downloads\\句式.txt", "r", encoding="UTF-8"):
        try:
            items = line.strip("\n").strip("\t").split("\t")
            rate = items[1]

            items_length = items.__len__()

            for index in range(2, items_length):
                if index % 2 == 0:
                    word = items[index]
                    nature = items[index+1]

                    list_1.append(word + "***" + nature+"\t"+rate)
        except Exception as e:
            print(e)
    # 统计频次，并排序
    # list_new = Tool.frequency_calculate(list_1)
    # #写入文件
    # list_file = []
    # for i in list_new:
    # list_file.append("\t".join(map(str, i)))
    str_file = "\n".join(list_1)
    # str_file += "\n"

    f = open("C:\\Users\\cb\\Downloads\\句式2.txt", "a", encoding="UTF-8")
    f.write(str_file)
    f.close()
if __name__ == '__main__':
    frequency_record()