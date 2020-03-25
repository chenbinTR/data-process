# -*- coding: utf-8 -*-
# import sys
# sys.path.append("/mnt/home/appuser/cbpython/tools/tool.py")
path = '/mnt/home/appuser/log201806-3/'


# 根据规则读取日志文件，提取所需要的内容，写入新的文件
def get_content():
    list_0 = list()
    for line in open(path+"statistics_result.txt", "r"):
        try:
            item_list = line.split("\t")
            apikey = item_list[0]
            num = item_list[1].strip("\n")
            try:
                userid = int(apikey)
                rate = int(num)
                if rate<10000:
                    continue
            except Exception as e1:
                str(e1)
                continue
            list_0.append(apikey)
        except Exception as e:
            str(e)
            print(str(e))

    print(list_0.__len__())

    list_1 = list()
    list_left = list()
    count = 0
    for line in open(path+"userid_result.txt", "r"):
        count += 1
        try:
            item_list = line.split("\t")
            apikey = item_list[0]
            try:
                userid = int(apikey)
                if userid < 1:
                    continue
            except Exception as e1:
                str(e1)
                continue
            if apikey in list_0:
                list_1.append(apikey+"\t" +item_list[5].strip().strip("\t").strip("\n")+"\t" +item_list[1].strip().strip("\t").strip("\n")+"\t" + item_list[2].strip().strip("\t").strip("\n"))
            else:
                list_left.append(line.strip("\n"))
        except Exception as e:
            str(e)
    print(list_1.__len__())
    str_file = "\n".join(list_1)
    f = open(path + 'res_100.txt', "w")
    f.write(str_file)
    f.close()

    str_left = "\n".join(list_left)
    f1 = open(path + 'userid_100.txt', "w")
    f1.write(str_left)
    f1.close()

if __name__ == '__main__':
    # 读取所有log文件路径
    # for log in logs:
    #     print(log)
        # print("processing......")
    get_content()
        # frequency_record()
    # 频次合并
    # combine_frequency()
    # 排序
    # Tool.sort_repeat(path, "combin_result.txt")
