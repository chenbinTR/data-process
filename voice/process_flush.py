# -*- coding: utf-8 -*-
# coding=utf-8
import os
from pydub import AudioSegment

# 对已上传oss的数据，执行增加静音段
# 输入路径 E:\BOOK_DATA\刷新数据\
# 输出路径 E:\BOOK_DATA\刷新数据-加静音段\


silence_times = 1000
silence_ring = AudioSegment.silent(int(silence_times))
source_list = []


# 为音频文件增加静音段
def addSilent(file):
    try:
        sound = AudioSegment.from_mp3(file)
        ring_lists = AudioSegment.empty()
        ring_lists += sound
        ring_lists += silence_ring

        dest_file = file.replace("刷新数据", "刷新数据-加静音段")

        ring_lists.export(dest_file, format="mp3")
    except Exception as e:
        print(e.__cause__)
        print(file)


# 处理一本书
def process_one_book(source):
    # 输出语音文件夹完整路径
    voice_dest_folder_path = source.replace("刷新数据", "刷新数据-加静音段")
    if not os.path.exists(voice_dest_folder_path):
        os.makedirs(voice_dest_folder_path)

    # 给音频文件增加结尾增加1s静音段
    for mp3 in os.listdir(source):
        path1 = os.path.join(source, mp3)
        addSilent(path1)


if __name__ == '__main__':
    source_folder = "E:\\BOOK_DATA\\刷新数据"
    for book in os.listdir(source_folder):
        if book == "url":
            continue
        source_list.append(book)
    # print(source_list)
    for book in source_list:
        source = os.path.join(source_folder, book)
        print(source)
        process_one_book(source)
        print(source+"---处理完成")
