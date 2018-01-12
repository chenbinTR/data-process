# -*- coding: utf-8 -*-
from tools.tool import *
path = ""
if __name__ == '__main__':
    set_chengyu = set()
    for line in open("Q:\\tmp\\成语库1.txt","r",encoding="UTF-8"):
        set_chengyu.add(line.strip("\n"))

    dict_continer = dict()
    list_result = list()
    for line in open(path + "20171026.txt", "r", encoding="UTF-8"):
        try:
            items = line.split("\t")
            que = items[0]
            time = items[5].strip("\n")

            if items[2] in dict_continer:
                str_line = dict_continer[items[2]][0]+"\t"+dict_continer[items[2]][1]+"\t"+dict_continer[items[2]][2]+"\t"+que+"\t"+time
                list_result.append(str_line)
                del dict_continer[items[2]]

            #若当前qa中q是成语
            if que in set_chengyu and items[3] == "2300102" and items[4] == "37" and items[2].__len__()>4:
                print(que, items[3] ,items[4])
                list_temp = list()
                list_temp.append(que)
                list_temp.append(items[1])
                list_temp.append(time)
                dict_continer[items[2]] = list_temp
            continue
        except Exception as e:
            # print(line)
            I = 1

    str_file = "\n".join(list_result)

    f = open("Q:\\result_chengyu.txt", "a", encoding="UTF-8")
    f.write(str_file)
    f.close()
