def sort_repeat():
    file_path = "Q:\\data\\中心词\\9月1\\"
    list_new = list()
    for line in open(file_path+"combin_result.txt", "r", encoding="UTF-8"):
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

    f = open(file_path+"sort_result.txt", "a", encoding="UTF-8")
    f.write(str_file)
    f.close()

def rate_caculate():
    count = 0
    rate_count = 0

    count_all = 0
    rate_count_all = 0

    for line in open("Q:\\data\\中心词\\9月\\sort_result.txt", "r", encoding="UTF-8"):
        item = line.split("\t")
        rate = int(item[1].strip("\n"))

        count_all += 1
        rate_count_all += rate
        if rate >= 20:
            count += 1
            rate_count += rate
    print(count,"----", rate_count)
    print(count_all,"-----", rate_count_all)


if __name__ == '__main__':
    # dict1 = dict()
    # dict1["你好"] = 1
    # dict1["不好"] = 2
    #
    # value = dict1.get("你好的")
    # if value:
    #     print(value)
    # else:
    #     print("no this key")
    #
    # test_str = "你好|干嘛呢|"
    # print(test_str.strip("|"))
    sort_repeat()
