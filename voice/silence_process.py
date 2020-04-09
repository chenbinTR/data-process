# -*- coding: utf-8 -*-
# coding=utf-8
from pydub import AudioSegment
import os

# get rings' directory and silence time
# directory = input("please input the rings' directory:")
directory = "E:\\BOOK_DATA\\刷新数据-加静音段"
# dest = "E:\\河北小学英语1起-result\\sss\\AudioByPage"
# silence_times = 1000*int(input("please input the silenct time(s) between two rings:"))
silence_times = 3000
print(directory)
print(silence_times)

# if not os.path.exists(dest):
#     os.makedirs(dest)
# delete ring_lists file
# if os._exists(directory+os.sep+"ring_lists.mp3"):
#     os.remove(directory+os.sep+"ring_lists.mp3")

silence_ring = AudioSegment.silent(int(silence_times))

# 转单声道
# ring_lists = AudioSegment.from_mp3("E:\\BOOK_DATA\\刷新数据-加静音段\\PEP人教小学英语-page\\37350\\1.mp3")
#
# single_ring = ring_lists.split_to_mono()[0]
# single_ring.export("E:\\1.mp3", format="mp3")

for page_folder in os.listdir(directory):
    if not page_folder.__contains__("河北"):
        continue
    try:
        page_folder_path = os.path.join(directory, page_folder)
        print(page_folder_path)
        for book_id in os.listdir(page_folder_path):
            book_id_path = os.path.join(page_folder_path, book_id)

            dest_path = book_id_path.replace("刷新数据-加静音段","刷新数据-加静音段-1")

            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            for mp3_name in os.listdir(book_id_path):
                mp3_name_path = os.path.join(book_id_path, mp3_name)
                ring_lists = AudioSegment.from_mp3(mp3_name_path)
                single_ring = ring_lists.split_to_mono()[0]
                single_ring.export(mp3_name_path.replace("刷新数据-加静音段","刷新数据-加静音段-1"), format="mp3")

        # sound = AudioSegment.from_mp3(path)
        # ring_lists = AudioSegment.empty()
        # ring_lists += silence_ring
        # ring_lists += sound
        # ring_lists.export(dest+os.sep+file, format="mp3")
    except Exception as e:
        print(e)

# get the audio files
# sounds = []
# for file in file_list:
#     sounds.append(AudioSegment.from_mp3(file))

# generate a silence ring file
# silence_ring = AudioSegment.silent(int(silence_times))

# merge the rings mixed with silence file
# ring_lists = AudioSegment.empty()
# i = 0
# for sound in sounds:
#     ring_lists = AudioSegment.empty()
#     # i += 1
#     ring_lists += sound
#     # if i!= sounds.__len__():
#     ring_lists += silence_ring
#
#     ring_lists.export(dest+os.sep+, format="mp3")