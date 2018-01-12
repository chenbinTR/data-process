

key = "鹿晗"

def is_end_or_start(word):
    if word in ("。","？"," ","\t","！"):
        return True
    return False



def get_words_by_article():
    #按行读取文件
    for line in open("Q:\\news.txt","r",encoding="UTF-8"):
        line = line.strip("\n")
        line = line.replace("\t","")
        line = line.replace("\n","")
        line = line.replace(" ","")
        line = line.replace("　","")
        ssss(line)


def ssss(line):
    while key in line:
        # 获取关键词所在的位置
        index_key = int(line.index(key))

        # 获取关键词前面的内容
        content_front = line[0:index_key]
        index_start = -1
        temp_num = -1
        for word in content_front:
            temp_num += 1
            if is_end_or_start(word):
                index_start = temp_num

        if index_start == -1:
            index_start = 0
        else:
            index_start+=1

        # 获取关键词后面的内容
        content_back = line[index_key + key.__len__():]
        index_end = -1
        temp_back_num = -1
        for word in content_back:
            temp_back_num += 1
            if is_end_or_start(word):
                index_end = temp_back_num
                break

        if index_end == -1:
            index_end = line.__len__()
        else:
            index_end += index_key+key.__len__()
        word_result = line[index_start:index_end]
        print(word_result)
        line = line[index_end:]


        f = open("Q:\\2.txt", "a", encoding="UTF-8")
        f.write(word_result+"\n")
        f.close()


if __name__ == '__main__':
    get_words_by_article()