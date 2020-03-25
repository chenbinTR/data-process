# -*- coding: utf-8 -*-
from tools.tool import *

path = 'C:\\Users\\cb\\Downloads\\'


# 读取待处理的内容，统计频次
def combin():
    dict_a = dict()
    for line in open(path + "log_children_parse_frequency.txt", "r", encoding="UTF-8"):
        try:
            items = line.strip("\n").split("\t")
            question = items[0]
            parse_type = items[1]
            value = items[2]

            temp_value = dict_a.get(question)

            if temp_value is None:
                temp_value = list()
                temp_value.append(parse_type + "\t" + value)
            else:
                temp_value.append(parse_type + "\t" + value)

            dict_a[question] = temp_value
        except Exception as e:
            print("11111111111111111111111")
            print(e)
            print(line)

    print(dict_a.__len__())

    list_re = list()
    count = 1
    for line in open(path + "log_children_frequency.txt", "r", encoding="UTF-8"):
        result = line.strip("\n")
        # print(count)
        # count += 1
        try:
            items = line.strip("\n").split("\t")
            question = items[0]
            value = int(items[1])

            if value < 10:
                continue

            temp_dict_value = dict_a.get(question)
            if temp_dict_value is not None:
                list_re.append(result + "\t" +"\t".join(list(temp_dict_value)))
            else:
                print("error ",question)

        except Exception as e:
            print("99999999999999999999")
            print(e)
            print(line)

    str_file = "\n".join(list_re)
    f = open(path + 'children_result.txt', "a", encoding="UTF-8")
    f.write(str_file)
    f.close()

# 根据规则读取日志文件，提取所需要的内容，写入新的文件
def get_log():
    file_name = path + "201904_log.txt"
    list_adult = list()
    list_children = list()
    count = 1
    for line in open(file_name, "r", encoding="UTF-8"):
        count += 1
        print(count)
        try:
            item_list = line.strip("\n").split("\t")
            question = item_list[0]
            appkey = item_list[1]
            parsetype = item_list[2]
            version = item_list[3]
            if not parsetype.isdigit():
                continue
            if appkey == "os.sys.chat" and version == "1.6":
                list_children.append(question + "\t" + parsetype)
                continue
            if appkey == "platform.chat" and version in ("2.0", "p1.0"):
                list_adult.append(question + "\t" + parsetype)
        except Exception as e:
            print(str(e))
            print("当前行： " + line)

    str_file = "\n".join(list_children)
    f = open(path + 'log_children.txt', "a", encoding="UTF-8")
    f.write(str_file)
    f.close()

    str_file = "\n".join(list_adult)
    f = open(path + 'log_adult.txt', "a", encoding="UTF-8")
    f.write(str_file)
    f.close()


# 读取待处理的内容，统计频次
def frequency_record():
    list_1 = []
    for line in open(path + "log_adult.txt", "r", encoding="UTF-8"):
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

    f = open(path + "log_adult_parse_frequency.txt", "a", encoding="UTF-8")
    f.write(str_file)
    f.close()

    # os.remove(path + "extract_data.txt")


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
    combin()
    # get_log()
    # 读取所有log文件路径
    # logs = Tool.get_all_files(path)
    # for log in logs:
    #     print(log)
    # print("processing......")
    # 根据规则提取原始日志文件
    # get_content(log)
    # 单个文件频次统计
    # frequency_record()
    # 频次合并
    # combine_frequency()
    # 排序
    # Tool.sort_repeat(path, "combin_result.txt")
    # dict_1 = dict()
    # dict_1["a"] = 1
    #
    # value = dict_1.get("a")

    # print(value)
