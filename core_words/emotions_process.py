# -*- coding: utf-8 -*-
from tools.tool import *



def rate_caculate():
    # 读取日志，根据关键词筛选日志
    logs = Tool.get_all_files("C:\\Users\\cb\\Downloads\\20171026\\")
    set_result = set()
    set_que = set()
    for log in logs:
        print(log)
        print("processing......")
        for line in open(log, "r", encoding="UTF-8"):
            try:
                items = line.split("\t");
                if items[1].__len__() < 21:
                    que = Tool.replaceAll(items[1], "\\[.+?\\]", "")
                    ci = Tool.is_contains_chinese(que)
                    if ci and "{" not in que:
                        # print(que)
                        set_result.add(que)
            except Exception as e:
                print(e)
    str_file = "\n".join(set_result)

    f = open("Q:\\产品\\情绪\\日志.txt", "a", encoding="UTF-8")
    f.write(str_file)
    f.close()


def get_que_by_key():

    # 读取关键词
    file_object = open('Q:\\产品\\情绪\\接纳.txt', encoding="UTF-8")
    keys = file_object.read()
    print(keys)


    # 读取日志，根据关键词筛选日志
    logs = Tool.get_all_files("C:\\Users\\cb\\Downloads\\1\\")
    set_result = set()
    set_que = set()
    for log in logs:
        print(log)
        print("processing......")
        for line in open(log, "r", encoding="UTF-8"):
            try:
                items = line.split("\t");
                if items[1] in ("2300101", "2300102") and items[0].__len__() < 20:
                    que = Tool.replaceAll(items[0], "\\[.+?\\]", "")
                    key = Tool.words_is_contains_keys(que, keys)
                    if key and que not in set_que:
                        set_que.add(que)
                        set_result.add(que+"\t"+key)
            except Exception as e:
                print(e)
    str_file = "\n".join(set_result)

    f = open("Q:\\产品\\情绪\\接纳-result.txt", "a", encoding="UTF-8")
    f.write(str_file)
    f.close()



def get():

    # 读取关键词
    # set_key = set()
    # for line in open('C:\\Users\\cb\\Downloads\\a\\情绪.txt', "r",encoding="UTF-8"):
    #     set_key.add(line.split("\t")[0])



    # 读取日志，根据关键词筛选日志
    set_que = set()
    for line in open("C:\\Users\\cb\\Downloads\\a\\rrrr.txt", "r", encoding="UTF-8"):
        try:
            que = line.strip("\n")
            if que.__len__()>20:
                continue
            set_que.add(que)
        except Exception as e:
            print(e)
    str_file = "\n".join(set_que)

    f = open("C:\\Users\\cb\\Downloads\\a\\rrrrdfdfd.txt", "a", encoding="UTF-8")
    f.write(str_file)
    f.close()


if __name__ == '__main__':
    # rate_caculate()
    # get()
    get_que_by_key()