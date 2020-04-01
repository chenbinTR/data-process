# -*- coding: utf-8 -*-
# coding=utf-8
from pydub import AudioSegment
import os, shutil

# 对博尔原始数据增加静音段
# 输入路径 E:\BOOK_DATA\已处理\已修正\
# 输出路径 E:\BOOK_DATA\已处理\已修正-加静音段

silence_times = 1000

silence_ring = AudioSegment.silent(int(silence_times))

source_list = ["陕西旅游出版社小学英语", "上海牛津小学英语深圳版", "新标准1起", "新标准3起", "译林牛津小学英语"]

source_name = "已修正"
dest_name = "已修正-加静音段"

# 为音频文件增加静音段
def addSilent(file):
    try:
        if os.path.isdir(file):
            return
        sound = AudioSegment.from_mp3(file)
        ring_lists = AudioSegment.empty()
        ring_lists += sound
        ring_lists += silence_ring

        dest_file = file.replace(source_name, dest_name)

        ring_lists.export(dest_file, format="mp3")
    except Exception as e:
        print(e.__cause__)
        print(file)

# 处理一本书
def process_one_book(source):
    for book_folder in os.listdir(source):
        # book文件夹完整路径
        book_folder_path = os.path.join(source, book_folder)
        # 语音 文件夹完整路径
        voice_path = os.path.join(source, book_folder, "语音")

        # 输出语音文件夹完整路径
        voice_dest_folder_path = voice_path.replace(source_name, dest_name)
        if not os.path.exists(voice_dest_folder_path):
            os.makedirs(voice_dest_folder_path)

        # copy其他文件夹和文件到目标book文件中
        for content in os.listdir(book_folder_path):
            content_path = os.path.join(book_folder_path, content)
            if os.path.isfile(content_path):
                shutil.copy(content_path, content_path.replace(source_name, dest_name))
            else:
                if content == "语音":
                    continue
                shutil.copytree(content_path, content_path.replace(source_name, dest_name))

        print(voice_path)

        # 给音频文件增加结尾增加1s静音段
        for mp3 in os.listdir(voice_path):
            path1 = os.path.join(voice_path, mp3)
            addSilent(path1)

for book in source_list:
    source = "E:\\BOOK_DATA\\已处理\\"+source_name+"\\"+book
    process_one_book(source)