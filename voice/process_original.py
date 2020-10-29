# -*- coding: utf-8 -*-
# coding=utf-8
from pydub import AudioSegment
import os, shutil
import uuid

# 对博尔原始数据增加静音段
# 输入路径 E:\BOOK_DATA\已处理\已修正\
# 输出路径 E:\BOOK_DATA\已处理\已修正-加静音段

# 根目录
root_path = "E:\\BOOK_DATA\\已处理\\已修正\\"

# 静音段
silence_times = 1000
silence_ring = AudioSegment.silent(int(silence_times), 44100)
# silence_ring = AudioSegment.from_mp3("E:\\jingyin1.mp3")
# silence_ring = silence_ring.split_to_mono()[0]
#
# source_list = ["北师大小学英语1起","教科版广州小学英语","河北小学英语1起","河北小学英语3起","科普小学英语","牛津上海版试用本","人教小学英语精通版","人教新起点","上海牛津小学英语深圳版","新标准1起","新标准3起","译林牛津小学英语"]

# 需要处理的书本名称
source_list = ['人教部编版语文456年级上册2020年秋河北印刷']
# source_list = []

# for book_name in os.listdir(root_path):
#     source_list.append(book_name)

source_name = "已修正"
dest_name = "已修正-加静音段"


# 为音频文件增加静音段
def addSilent(file):
    try:
        if os.path.isdir(file):
            return
        sound = AudioSegment.from_mp3(file)
        sound = sound.split_to_mono()[0]
        # print('channels: ', sound.channels, "-", silence_ring.channels)
        # print("frame_rate: ", sound.frame_rate, '-', silence_ring.frame_rate)
        # print("sample_width: ", sound.sample_width, "-", silence_ring.sample_width)
        # print("frame_width: ", sound.frame_width, "-", silence_ring.frame_width)
        # print()
        # print(sound.frame_width)
        # ring_lists = AudioSegment.empty()
        # ring_lists += sound
        # ring_lists += sound.split_to_mono()[0]
        # ring_lists += silence_ring
        sound += silence_ring
        dest_file = file.replace(source_name, dest_name)
        # cmd = 'ffmpeg -i "concat:'+file+'|E:\\jingyin.mp3" -acodec copy '+dest_file
        # os.system(cmd)

        # 转单声道
        # single_ring = ring_lists.split_to_mono()[0]
        # ring_lists.export(dest_file, format="mp3")
        sound = sound.split_to_mono()[0]
        sound.export(dest_file, format="mp3")

    except Exception as e:
        print(e,file)


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
            if not mp3.lower().endswith("mp3"):
                continue
            path1 = os.path.join(voice_path, mp3)
            addSilent(path1)


for book in source_list:
    source = root_path + book
    process_one_book(source)
