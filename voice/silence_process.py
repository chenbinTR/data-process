from pydub import AudioSegment
import os

# get rings' directory and silence time
# directory = input("please input the rings' directory:")
directory = "C:\\Users\\cb\\Downloads\\shanghainiujin\\shanghainiujin"
dest = "C:\\Users\\cb\\Downloads\\shanghainiujin\\shanghainiujin-new"
# silence_times = 1000*int(input("please input the silenct time(s) between two rings:"))
silence_times = 1000
print(directory)
print(silence_times)

# delete ring_lists file
# if os._exists(directory+os.sep+"ring_lists.mp3"):
#     os.remove(directory+os.sep+"ring_lists.mp3")

silence_ring = AudioSegment.silent(int(silence_times))

# get files' name
# file_list = []
for file in os.listdir(directory):
    try:
        path = os.path.join(directory, file)
        sound = AudioSegment.from_mp3(path)

        ring_lists = AudioSegment.empty()
    # i += 1
        ring_lists += sound
    # if i!= sounds.__len__():
        ring_lists += silence_ring
        ring_lists.export(dest+os.sep+file, format="mp3")
    except Exception as e:
        print(file)

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