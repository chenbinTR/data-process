import requests
import os
from random import choice
import random
from tools.tool import *

# html = requests.get("http://www.qiushibaike.com")
#
# print(html.content)

path = "C:\\Users\\cb\\Downloads\\20170510\\"
path_out = "C:\\Users\\cb\\Downloads\\mp3\\"

if __name__ == '__main__':

    list_result = list()
    for line in open("C:\\Users\\cb\\Downloads\\sort_result.txt","r",encoding="UTF-8"):
        item = line.strip("\n").replace("\\n","")
        if line.__contains__("topic"):
            item = item[item.index("}")+1:]
            print(item)
        list_result.append(item)

    print(list_result.__len__())
    str_file = "\n".join(list_result)

    f = open("C:\\Users\\cb\\Downloads\\sort_result_new.txt", "a",encoding="UTF-8")
    f.write(str_file)
    f.close()