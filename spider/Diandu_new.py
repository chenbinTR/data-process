# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 13:53:17 2019

@author: zzhqi
"""

import urllib
import re
import os
import PIL.Image as Image
from pydub import AudioSegment
import functools
import shutil
import pandas as pd


def getHTML(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    html = html.decode('utf-8')
    return html

def getVersionUrlList(html):
    versions = re.findall("<a href=\"(.*?)html\"",html)
    for i in range(len(versions)):
        versions[i] = versions[i]+"html"
    return versions

def getBookID(html):
    booksID = re.findall("href=\"http://www.1010jiajiao.com/diandu/book/(.*?).html",html)
    return booksID

def getBookNameList(html):
    names = re.findall("span class=\"tt\">(.*?)<",html)
    return names

def getTracksDF(html):
    df = pd.DataFrame(columns = ["y1","x2","y2","x1","start","end","chapter","page"])
    tracks = re.findall("var tracks  =(.*?);",html)[0]
    tracks = tracks[1:len(tracks)-1]
    trackList = tracks.split("[")[1:]
    for track in trackList:
        track = re.sub("[\[\]\"]","",track)
        track = track.strip(",")
        tupleList = track.split(",")
        #if tupleList[7]!="null":     
#            df.loc[len(df)] = [float(tupleList[0]),float(tupleList[1]),float(tupleList[2]),
#               float(tupleList[3]),float(tupleList[5]),float(tupleList[6]),int(tupleList[7]),
#               int(tupleList[8])]
        #else:
#            df.loc[len(df)] = [str(tupleList[0]),str(tupleList[1]),str(tupleList[2]),
#               str(tupleList[3]),str(tupleList[5]),str(tupleList[6]),str(tupleList[7]),
#               int(tupleList[8])]
        if tupleList[0] != "null":
            float(tupleList[0])
        if tupleList[1] != "null":
            float(tupleList[1])
        if tupleList[2] != "null":
            float(tupleList[2])
        if tupleList[3] != "null":
            float(tupleList[3])   
        if tupleList[5] != "null":
            float(tupleList[5])   
        if tupleList[6] != "null":
            float(tupleList[6])   
        if tupleList[7] != "null":
            int(tupleList[7])  
        int(tupleList[8])
            
        df.loc[len(df)] = [str(tupleList[0]),str(tupleList[1]),str(tupleList[2]),
               str(tupleList[3]),str(tupleList[5]),str(tupleList[6]),str(tupleList[7]),
               int(tupleList[8])]     #统一格式加入dataFrame 需要时再转换
    return df

def addActualPageColToDF(offSet,tracksDF):
    for i in range(0,len(tracksDF)):
        tracksDF["actualPage"] = tracksDF["page"]+offSet
    print("Add the actual page list column to dataframe successfully.")

def getImgUrlList(tracksDF,bookID):
    imgUrlList = []
    maxPossiblePage = int(tracksDF["page"][len(tracksDF)-1])+10
    for i in range(0,maxPossiblePage+1):
        if i<10:
            page = "00"+str(i)
        elif 10<=i<100:
            page = "0"+str(i)
        elif i>=100:
            page = str(i)
        imgUrlList.append("http://thumb.1010pic.com/dmt/diandu/"+bookID+"/page/"+page+".jpg?v=7")
    return imgUrlList

def downloadImg(tracksDF,urlList,path):
    x = 0
    offSet = 0
    assignOffSet = False
    print("Start downloading images...")
    for url in urlList:
        try:
            urllib.request.urlretrieve(url,'{}{}.jpg'.format(path,x))
            print("Page "+ str(x) +" has been downloaded.")
            if offSet == 0 and assignOffSet==False:
                offSet = x
                assignOffSet = True
        except Exception:
            print("Page not included!")
        x = x+1
    print("Finish downloading images.")
    return offSet

def downloadCoverPage(bookID,path):
    url = "http://thumb.1010pic.com/dmt/diandu/"+bookID+"/cover.jpg?v=7"
    urllib.request.urlretrieve(url,'{}{}.jpg'.format(path,0))
    print("Cover has been downloaded.")

def downloadAudio(urlList,path):
    x = 0
    print("Start downloading audio...")
    for url in urlList:
        # just for special case
        url = url.replace('    "','').replace('"','')
        print(url)

        url = urllib.parse.quote(url,safe=':/')  #将url里的中文以及空格转换为ascii能识别的字符
        print(url)
        #just for special case
        # url = url.replace('%0A%20%20%20','')
        try:
            urllib.request.urlretrieve(url,'{}{}.mp3'.format(path,x))
        except Exception:
            print("download " + url + "has wrong audio url\n")
            file = open(r"C:\zhaopeng\daniel\turingos\Diandu_Books\log.txt","a")
            file.write(url)
            file.write('\n')
            file.close()
        x = x+1
    print("Finish downloading audio.")


def make_dir(folder):
    path = os.getcwd() + "/" + folder
    if not os.path.isdir(path):
        os.makedirs(path)
    return path

def mergeImgs(tracksDF,pathFrom,pathTo):
    print("Start merging images...")
    x = 1           #若合并后图片序号与管理平台中绘本页数对不上，需调整x(极少数情况)
    for i in range(tracksDF["actualPage"][0],tracksDF["actualPage"][len(tracksDF)-1]+1):
        if i%2 != 0:
            if i==1 and tracksDF["actualPage"][0] != 0:
                imgSingle = Image.open(pathFrom+str(i)+".jpg")
                imgSingle.save(pathTo+str(x)+"-"+str(imgSingle.width)+"-"+str(imgSingle.height)+".jpg")
                x = x+1
                print("Single page.")
        elif i%2 == 0:
            if i==int(tracksDF["actualPage"][len(tracksDF)-1]):
                try:
                    imgSingle = Image.open(pathFrom+str(i)+".jpg")
                    imgSingle.save(pathTo+str(x)+"-"+str(imgSingle.width)+"-"+str(imgSingle.height)+".jpg")
                    x = x+1
                    print("Single page.")
                except Exception:
                    print("Jumped page!")
                    x = x+1
                    continue
            else:
                try:
                    imgLeftPage = Image.open(pathFrom+str(i)+".jpg")  
                    imgRightPage = Image.open(pathFrom+str(i+1)+".jpg")
                    toImage = Image.new('RGB', (imgLeftPage.width+imgRightPage.width, max(imgLeftPage.height,imgRightPage.height)))
                    # toImage = Image.new('RGB', (imgLeftPage.width+imgRightPage.width, imgLeftPage.height))   左右页高度不同
                    # 可改成下对齐，当前为上对齐
                    toImage.paste(imgLeftPage,(0,0))
                    toImage.paste(imgRightPage,(imgLeftPage.width,0))
                    toImage.save(pathTo+str(x)+"-"+str(toImage.width)+"-"+str(toImage.height)+".jpg")
                    x = x+1
                    print("Double page.")
                except Exception:
                    print("Jumped page!")
                    try:
                        imgSingle = Image.open(pathFrom+str(i)+".jpg")
                        imgSingle.save(pathTo+str(x)+"-"+str(imgSingle.width)+"-"+str(imgSingle.height)+".jpg")
                        x = x+1
                        print("Single page.")
                    except Exception:
                        x = x+1
                        continue
    print("Finish merging images.")
       
    
def cutAudio(tracksDF,pathFrom,pathTo):
    print("Start cutting audio ...")
    for i in range(0,len(tracksDF["chapter"])):     # 0 ~ (len-1) 遍历整个dataframe
        if tracksDF["chapter"][i] == "null":
            continue
        else:  
            audio = AudioSegment.from_mp3(pathFrom + tracksDF["chapter"][i] +".mp3")
            start_time = float(tracksDF["start"][i])*1000 - 2000 - 150  #分割音频有时会有点损坏头尾，补一点
            end_time = float(tracksDF["end"][i])*1000 - 2000 + 350
            audioSeg = audio[start_time:end_time]
            if(tracksDF["actualPage"][0]%2 == 0):
                if(tracksDF["actualPage"][i]%2 == 0):
                    if(tracksDF["actualPage"][i]==tracksDF["actualPage"][len(tracksDF)-1]):  #single page(if the last page number is even)
                        save_name = str(int((tracksDF["actualPage"][i]-tracksDF["actualPage"][0])/2)+1)+"-"+str(tracksDF["x1"][i])+"-"+str(tracksDF["y1"][i])+"-"+str(tracksDF["x2"][i])+"-"+str(tracksDF["y2"][i])+"-"+str(i)+".mp3"  # 页数-x1-y1-x2-y2-id.mp3
                        #print("Last page is single and even.")
                    else:
                        save_name = str(int((tracksDF["actualPage"][i]-tracksDF["actualPage"][0])/2)+1)+"-"+str(float(tracksDF["x1"][i])/2)+"-"+str(tracksDF["y1"][i])+"-"+str(float(tracksDF["x2"][i])/2)+"-"+str(tracksDF["y2"][i])+"-"+str(i)+".mp3"  # 页数-x1-y1-x2-y2-id.mp3
                        #print("Even page.")
                else:
                    if(tracksDF["actualPage"][i]==tracksDF["actualPage"][0]):  #single page(if the first page number is odd)
                        save_name = str(int((tracksDF["actualPage"][i]-tracksDF["actualPage"][0])/2)+1)+"-"+str(tracksDF["x1"][i])+"-"+str(tracksDF["y1"][i])+"-"+str(tracksDF["x2"][i])+"-"+str(tracksDF["y2"][i])+"-"+str(i)+".mp3"  # 页数-x1-y1-x2-y2-id.mp3
                        #print("First page is single and odd.")
                    else:
                        save_name = str(int((tracksDF["actualPage"][i]-tracksDF["actualPage"][0])/2)+1)+"-"+str(float(tracksDF["x1"][i])/2+0.5)+"-"+str(tracksDF["y1"][i])+"-"+str(float(tracksDF["x2"][i])/2+0.5)+"-"+str(tracksDF["y2"][i])+"-"+str(i)+".mp3"  # 页数-x1-y1-x2-y2-id.mp3
                        #print("Odd page.")
            elif(tracksDF["actualPage"][0]%2 != 0):
                if(tracksDF["actualPage"][i]%2 == 0):
                    if(tracksDF["actualPage"][i]==tracksDF["actualPage"][len(tracksDF)-1]):  #single page(if the last page number is even)
                        save_name = str(int((tracksDF["actualPage"][i]-tracksDF["actualPage"][0]+1)/2)+1)+"-"+str(tracksDF["x1"][i])+"-"+str(tracksDF["y1"][i])+"-"+str(tracksDF["x2"][i])+"-"+str(tracksDF["y2"][i])+"-"+str(i)+".mp3"  # 页数-x1-y1-x2-y2-id.mp3
                        #print("Last page is single and even.")
                    else:
                        save_name = str(int((tracksDF["actualPage"][i]-tracksDF["actualPage"][0]+1)/2)+1)+"-"+str(float(tracksDF["x1"][i])/2)+"-"+str(tracksDF["y1"][i])+"-"+str(float(tracksDF["x2"][i])/2)+"-"+str(tracksDF["y2"][i])+"-"+str(i)+".mp3"  # 页数-x1-y1-x2-y2-id.mp3
                        #print("Even page.")
                else:
                    if(tracksDF["actualPage"][i]==tracksDF["actualPage"][0]):  #single page(if the first page number is odd)
                        save_name = str(int((tracksDF["actualPage"][i]-tracksDF["actualPage"][0]+1)/2)+1)+"-"+str(tracksDF["x1"][i])+"-"+str(tracksDF["y1"][i])+"-"+str(tracksDF["x2"][i])+"-"+str(tracksDF["y2"][i])+"-"+str(i)+".mp3"  # 页数-x1-y1-x2-y2-id.mp3
                        #print("First page is single and odd.")
                    else:
                        save_name = str(int((tracksDF["actualPage"][i]-tracksDF["actualPage"][0]+1)/2)+1)+"-"+str(float(tracksDF["x1"][i])/2+0.5)+"-"+str(tracksDF["y1"][i])+"-"+str(float(tracksDF["x2"][i])/2+0.5)+"-"+str(tracksDF["y2"][i])+"-"+str(i)+".mp3"  # 页数-x1-y1-x2-y2-id.mp3
                        #print("Odd page.")
            audioSeg.export(pathTo+save_name, format="mp3")
            print("Audio segement "+str(i)+" has been cutted.")
    print("Finish cutting audio.")
    
#def mergeAudio(tracksDF,pathFrom,pathTo):  #不用这个
#    #获取每页（双页）的音频，有两种方案，一种为mergeAudio即将分割过的音频片段拼接，缺点是拼不全，运行速度慢。
#    #另一种为cutAudioByPage，直接用chapter音频切割
#    print("Start merging audio...")
#    flag = 0
#    audioMerged = 0 
#    path_list = os.listdir(pathFrom) #待读取的文件夹
#    path_list.sort(key=functools.cmp_to_key(audioSegmentsSortRule)) #对读取的路径进行排序
#    for filename in path_list:	
#        print(os.path.join(pathFrom,filename))
#    for index,i in enumerate(path_list):
#        for j in range(1,int(tracksDF["page"][len(tracksDF)-1]/2)+3):
#            if j == int(i.split("-")[0]):
#                if flag != j and flag != 0:
#                    audioMerged.export(pathTo+path_list[index-1].split("-")[0]+".mp3")
#                    audioMerged = 0 
#                flag = j
#                pause = 0
#                try:
#                    audio = AudioSegment.from_mp3(pathFrom + i)
#                except Exception:
#                    print("Audio file is damaged!")
#                    
#                    break
#                if index==0:
#                    pause = AudioSegment.silent(duration=1500)
#                else:
#                    indexOfDF = int(i.split("-")[-1][:-4])
#                    lastIndexOfDF = int(path_list[index-1].split("-")[-1][:-4])
#                    if tracksDF["start"][indexOfDF] < tracksDF["end"][lastIndexOfDF]:  #若更换章节了
#                        pause = AudioSegment.silent(duration=1500)
#                    else:
#                        pauseDuration = (float(tracksDF["start"][indexOfDF]) - float(tracksDF["end"][lastIndexOfDF]))*1000
#                        if pauseDuration>2000:
#                            pauseDuration = 2000    #避免过长的间隔时间
#                        pause = AudioSegment.silent(duration=pauseDuration)
#                audioMerged = audioMerged + pause + audio
#                if(index==len(path_list)-1):
#                    audioMerged.export(pathTo+path_list[index-1].split("-")[0]+".mp3")
#                break
#        print(i+" has been merged.")
#    print("Finish merging audio.")
    
def cutAudioByPage(tracksDF,pathFrom,pathTo):   #获取每页音频时用这个方法
    print("Start cutting audio by page...")
    flag = 0 
    startTime = 0
    endTime = 0 
    #chapter = 0
    audioSegByPage = 0
    boundaryIndex = 0
    startFrom = 1
    characterChanged = False
    newPage = True
    path_list = os.listdir(pathFrom + "AudioSegments/")
    path_list.sort(key=functools.cmp_to_key(audioSegmentsSortRule)) #对读取的路径进行排序
#    for filename in path_list:	
#        print(os.path.join(pathFrom + "AudioSegments/",filename))
    for index,i in enumerate(path_list):
        for j in range(startFrom,int(tracksDF["page"][len(tracksDF)-1]/2)+3):
            if j == int(i.split("-")[0]):  
                if (flag != j and flag != 0) or index==len(path_list)-1:  #如果换页或者到了最后一页
                    if(index==len(path_list)-1):  #如果最后一页，直接把最后一个音频播放完
                        endTime = 99999999
                    else:
                        endTime = float(tracksDF["end"][int(path_list[index-1].split("-")[-1][:-4])])*1000 - 2000 + 1500
                    if(characterChanged):
                        audio1 = AudioSegment.from_mp3(pathFrom + "sourceAudio/" + str(tracksDF["chapter"][int(path_list[boundaryIndex].split("-")[-1][:-4])]) + ".mp3")
                        audio2 = AudioSegment.from_mp3(pathFrom + "sourceAudio/" + str(tracksDF["chapter"][int(path_list[index-1].split("-")[-1][:-4])]) +".mp3")
                        pause = AudioSegment.silent(duration=500)
                        audioSegByPage = audio1[startTime:]+pause+audio2[:endTime]
                        audioSegByPage.export(pathTo+path_list[index-1].split("-")[0]+".mp3", format="mp3")
                        
                        print("Audio of page "+path_list[index-1].split("-")[0]+" has been cutted(involve changing of character).")
                    else:
                        audio = AudioSegment.from_mp3(pathFrom + "sourceAudio/" + str(tracksDF["chapter"][int(path_list[index-1].split("-")[-1][:-4])]) +".mp3")
                        audioSegByPage = audio[startTime:endTime]
                        audioSegByPage.export(pathTo+path_list[index-1].split("-")[0]+".mp3", format="mp3")
                        print("Audio of page "+path_list[index-1].split("-")[0]+" has been cutted(not involve changing of character).") 
                    startTime = 0
                    boundaryIndex = index
                    startFrom = startFrom + 1
                    characterChanged = False
                    newPage = True  #方便之后判断换没换章节
                if startTime == 0:
                    startTime = float(tracksDF["start"][int(i.split("-")[-1][:-4])])*1000 - 2000 - 150
                    flag = j
                if newPage==False and characterChanged==False and float(tracksDF["start"][int(path_list[index].split("-")[-1][:-4])]) < float(tracksDF["start"][int(path_list[index-1].split("-")[-1][:-4])]): #若换章节了
#                    print(tracksDF["start"][int(path_list[index].split("-")[-1][:-4])]+"  "+str(path_list[index]))
#                    print(tracksDF["start"][int(path_list[index-1].split("-")[-1][:-4])]+"  "+str(path_list[index-1]))
                    #chapter = chapter + 1
                    if(int(tracksDF["chapter"][int(path_list[index].split("-")[-1][:-4])]) != int(tracksDF["chapter"][int(path_list[index-1].split("-")[-1][:-4])])):
                        characterChanged = True
                newPage = False
                break
    print("Finish cutting audio by page.")

def audioSegmentsSortRule(x,y):
    if int(x.split("-")[0]) > int(y.split("-")[0]):
        return 1
    elif int(x.split("-")[0]) < int(y.split("-")[0]):
        return -1
    else:
        if int(x.split("-")[-1][:-4]) > int(y.split("-")[-1][:-4]):
            return 1
        elif int(x.split("-")[-1][:-4]) < int(y.split("-")[-1][:-4]):
            return -1
        else:
            print("error!")

def downloadOneSetOfBooks(bookIDList):       #下载同一出版社的所有书
    for id in bookIDList:
        downloadOneBook(id)
    return

def downloadOneBook(bookID):       #下载单本书
    bookUrl = "http://www.1010jiajiao.com/diandu/book/"+bookID+".html"
    bookHTML = getHTML(bookUrl)
    bookName = re.findall("<title>(.*?)</title>",bookHTML)[0].split("——")[0]
    
    print("### Start processing book "+bookName+" ###")
    make_dir("./Diandu_Books/")
    # try:
    tracksDF = getTracksDF(bookHTML)  #若tracks格式有误 则下载下一本书
    # except Exception:
    #     print("Book "+bookName+" Script中tracks格式有误!")
    #     txtPath = "./Diandu_Books/"+bookName+" Script中tracks格式有误.txt"
    #     file = open(txtPath, 'w')
    #     file.close()
    #     return
        
    imgUrlList = getImgUrlList(tracksDF,bookID)

    audioUrlList = getAudioUrlList(bookHTML, bookID)

    try:
        audioUrlList = getAudioUrlList(bookHTML,bookID)
    except Exception:
        print("Book "+bookName+" has wrong audio url format!")
        txtPath = "./Diandu_Books/"+bookName+" 音频网址错误(转码错误).txt"
        file = open(txtPath, 'w')
        file.close()
        return
    offSet = downloadImg(tracksDF,imgUrlList,make_dir("./Diandu_Books/"+bookName+"/Bookimg/sourceimg/")) #书可能是从0，1，2，3...页开始的，需要在下载过程中来判断从哪页开始，获取与真实页数偏移值
    addActualPageColToDF(offSet,tracksDF)  #把真实页数添加到dataFrame中
    try:
        downloadAudio(audioUrlList,make_dir("./Diandu_Books/"+bookName+"/Audio/sourceAudio/"))
    except Exception:
        print("Book "+bookName+" has wrong audio url format!")
        txtPath = "./Diandu_Books/"+bookName+" 音频网址错误(HTTPNotFound).txt"
        file = open(txtPath, 'w')
        file.close()
        shutil.rmtree("./Diandu_Books/"+bookName)
        return
    mergeImgs(tracksDF,"./Diandu_Books/"+bookName+"/Bookimg/sourceimg/",make_dir("./Diandu_Books/"+bookName+"/Bookimg/Merge/"))

    if os.path.exists("./Diandu_Books/"+bookName+"/Bookimg/sourceimg/"):
        shutil.rmtree("./Diandu_Books/"+bookName+"/Bookimg/sourceimg/")
    downloadCoverPage(bookID,"./Diandu_Books/"+bookName+"/Bookimg/")
    cutAudio(tracksDF,"./Diandu_Books/"+bookName+"/Audio/sourceAudio/",make_dir("./Diandu_Books/"+bookName+"/Audio/AudioSegments/"))
    # try:

    cutAudioByPage(tracksDF,"./Diandu_Books/"+bookName+"/Audio/",make_dir("./Diandu_Books/"+bookName+"/Audio/AudioByPage/"))

    # except Exception:
    #     print("Book "+bookName+" may have repetitive audio segements name!")
    #     txtPath = "./Diandu_Books/"+bookName+" 在按页切割音频方法.音频片段排序时出错.可能片段名字有重复的.txt"
    #     file = open(txtPath, 'w')
    #     file.close()
    #     shutil.rmtree("./Diandu_Books/"+bookName)
    #     return
    if os.path.exists("./Diandu_Books/"+bookName+"/Audio/sourceAudio/"):
        shutil.rmtree("./Diandu_Books/"+bookName+"/Audio/sourceAudio/")
    print("### Book "+bookName+" finished! ###")

def getAudioUrlList(html, bookID):
    audioNames = re.findall("var map_id_mp3 =(.*?);", html)[0]
    audioNames = audioNames[2:len(audioNames) - 1]
    audioList = audioNames.split(",")
    # audioList =   ['"000001_\\u8bfe\\u6587_1. \\u53e4\\u8bd7\\u4e8c\\u9996.mp3"', '"000004_\\u8bfe\\u6587_2. \\u627e\\u6625\\u5929.mp3"', '"000006_\\u8bfe\\u6587_3. \\u5f00\\u6ee1\\u9c9c\\u82b1\\u7684\\u5c0f\\u8def.mp3"', '"000009_\\u8bfe\\u6587_4. \\u9093\\u5c0f\\u5e73\\u7237\\u7237\\u690d\\u6811.mp3"', '"000012_\\u8bfe\\u6587_\\u8bed\\u6587\\u56ed\\u5730\\u4e00.mp3"', '"000016_\\u8bfe\\u6587_5. \\u96f7\\u950b\\u53d4\\u53d4,\\u4f60\\u5728\\u54ea\\u91cc.mp3"', '"000019_\\u8bfe\\u6587_6. \\u5343\\u4eba\\u7cd5.mp3"', '"000022_\\u8bfe\\u6587_7. \\u4e00\\u5339\\u51fa\\u8272\\u7684\\u9a6c.mp3"', '"000025_\\u8bfe\\u6587_\\u8bed\\u6587\\u56ed\\u5730\\u4e8c.mp3"', '"000029_\\u8bc6\\u5b57_1. \\u795e\\u5dde\\u8c23.mp3"', '"000031_\\u8bc6\\u5b57_2. \\u4f20\\u7edf\\u8282\\u65e5.mp3"', '"000033_\\u8bc6\\u5b57_3. \\u8d1d\\u7684\\u6545\\u4e8b.mp3"', '"000035_\\u8bc6\\u5b57_4. \\u4e2d\\u56fd\\u7f8e\\u98df.mp3"', '"000038_\\u8bc6\\u5b57_\\u8bed\\u6587\\u56ed\\u5730\\u4e09.mp3"', '"000042_\\u8bfe\\u6587_8. \\u5f69\\u8272\\u7684\\u68a6.mp3"', '"000045_\\u8bfe\\u6587_9. \\u67ab\\u6811\\u4e0a\\u7684\\u559c\\u9e4a.mp3"', '"000048_\\u8bfe\\u6587_10. \\u6c99\\u6ee9\\u4e0a\\u7684\\u7ae5\\u8bdd.mp3"', '"000051_\\u8bfe\\u6587_11. \\u6211\\u662f\\u4e00\\u53ea\\u5c0f\\u866b\\u5b50.mp3"', '"000053_\\u8bfe\\u6587_\\u8bed\\u6587\\u56ed\\u5730\\u56db.mp3"', '"000057_\\u8bfe\\u6587_12. \\u5bd3\\u8a00\\u4e8c\\u5219.mp3"', '"000060_\\u8bfe\\u6587_13. \\u753b\\u6768\\u6843.mp3"', '"000063_\\u8bfe\\u6587_14. \\u5c0f\\u9a6c\\u8fc7\\u6cb3.mp3"', '"000068_\\u8bfe\\u6587_\\u8bed\\u6587\\u56ed\\u5730\\u4e94.mp3"', '"000071_\\u8bfe\\u6587_15. \\u53e4\\u8bd7\\u4e8c\\u9996.mp3"', '"000074_\\u8bfe\\u6587_16. \\u96f7\\u96e8.mp3"', '"000076_\\u8bfe\\u6587_17. \\u8981\\u662f\\u4f60\\u5728\\u91ce\\u5916\\u8ff7\\u4e86\\u8def.mp3"', '"000079_\\u8bfe\\u6587_18. \\u592a\\u7a7a\\u751f\\u6d3b\\u8da3\\u4e8b\\u591a.mp3"', '"000081_\\u8bfe\\u6587_\\u8bed\\u6587\\u56ed\\u5730\\u516d.mp3"', '"000086_\\u8bfe\\u6587_19. \\u5927\\u8c61\\u7684\\u8033\\u6735.mp3"', '"000089_\\u8bfe\\u6587_20. \\u8718\\u86db\\u5f00\\u5e97.mp3"', '"000092_\\u8bfe\\u6587_21. \\u9752\\u86d9\\u5356\\u6ce5\\u5858.mp3"', '"000096_\\u8bfe\\u6587_22. \\u5c0f\\u6bdb\\u866b.mp3"', '"000099_\\u8bfe\\u6587_\\u8bed\\u6587\\u56ed\\u5730\\u4e03.mp3"', '"000102_\\u8bfe\\u6587_23. \\u7956\\u5148\\u7684\\u6447\\u7bee.mp3"', '"000105_\\u8bfe\\u6587_24. \\u5f53\\u4e16\\u754c\\u5e74\\u7eaa\\u8fd8\\u5c0f\\u7684\\u65f6\\u5019.mp3"', '"000108_\\u8bfe\\u6587_25. \\u7fbf\\u5c04\\u4e5d\\u65e5.mp3"', '"000112_\\u8bfe\\u6587_\\u8bed\\u6587\\u56ed\\u5730\\u516b.mp3"']
    # audioList = ['"000001_Unit_1. School rules.mp3"', '"000008_Unit_2. A letter from Tommy\'s pen pal,Bella.mp3"', '"000015_Reading_1. Andy eats too much!.mp3"', '"000016_Unit_3. Sports and health.mp3"', '"000023_Unit_4. No one is perfect.mp3"', '"000031_Reading_2. Dogs at work.mp3"', '"000032_Unit_5. Grandpa\'s house.mp3"', '"000040_Unit_6. A story about the Wright brothers.mp3"', '"000048_Reading_3. Mr Watt and Mr Knott.mp3"', '"000049_Unit_7. Mingming\'s diary.mp3"', '"000056_Unit_8. A note to Mum and Dad.mp3"', '"000063_Reading_4. The cat and the fox.mp3"', '"000064_Unit_9. The weather report.mp3"', '"000072_Unit_10. The sun and the wind.mp3"', '"000080_Reading_5. A game you should not play.mp3"', '"000084_Word Bank_Unit 01.mp3"', '"000084_Word Bank_Unit 02.mp3"', '"000084_Word Bank_Unit 03.mp3"', '"000084_Word Bank_Unit 04.mp3"', '"000084_Word Bank_Unit 05.mp3"', '"000085_Word Bank_Unit 06.mp3"', '"000085_Word Bank_Unit 07.mp3"', '"000085_Word Bank_Unit 08.mp3"', '"000085_Word Bank_Unit 09.mp3"', '"000085_Word Bank_Unit 10.mp3"']
    # audioList = ['"000002_Module 1 Getting to know you_Unit 1.My birthday.mp3"', '"000007_Module 1 Getting to know you_Unit 2.My way to school.mp3"', '"000012_Module 1 Getting to know you_Unit 3.My future.mp3"', '"000017_Module 2 Me,my family and friends_Unit 1.Grandparents.mp3"', '"000022_Module 2 Me,my family and friends_Unit 2.Friends.mp3"', '"000027_Module 2 Me,my family and friends_Unit 3.Moving home.mp3"', '"000032_Module 3 Places and activities_Unit 1.Around the city.mp3"', '"000037_Module 3 Places and activities_Unit 2.Buying new clothes.mp3"', '"000042_Module 3 Places and activities_Unit 3.Seeing the doctor.mp3"', '"000047_Module 4 The natural world_Unit 1.Water.mp3"', '"000052_Module 4 The natural world_Unit 2.Wind.mp3"', '"000057_Module 4 The natural world_Unit 3.Fire.mp3"']
    # audioList = ['"000001_Unit 1 Sports_Lesson 1 Ping-pong and Basketball.mp3"', '"000004_Unit 1 Sports_Lesson 2 At the Sports Shop.mp3"', '"000006_Unit 1 Sports_Lesson 3 Let\'s Play.mp3"', '"000008_Unit 1 Sports_Lesson 4 Did You Have Fun.mp3"', '"000010_Unit 1 Sports_Lesson 5 A Basketball Game.mp3"', '"000012_Unit 1 Sports_Lesson 6 A Famous Football Player.mp3"', '"000014_Unit 1 Sports_Again Please.mp3"', '"000019_Unit 2 Good Health to You_Lesson 7 Always Have Breakfast.mp3"', '"000022_Unit 2 Good Health to You_Lesson 8 Always Brush Your Teeth.mp3"', '"000024_Unit 2 Good Health to You_Lesson 9 Eat More Vegetables and Fruit.mp3"', '"000026_Unit 2 Good Health to You_Lesson 10 Exercise.mp3"', '"000028_Unit 2 Good Health to You_Lesson 11 Work Hard.mp3"', '"000030_Unit 2 Good Health to You_Lesson 12 Helen Keller.mp3"', '"000032_Unit 2 Good Health to You_Again Please.mp3"', '"000037_Unit 3 What Will You Do This Summer_Lesson 13 Summer Is Coming.mp3"', '"000040_Unit 3 What Will You Do This Summer_Lesson 14 Tomorrow We Will Play.mp3"', '"000042_Unit 3 What Will You Do This Summer_Lesson 15 Jenny\'s Summer Holiday.mp3"', '"000044_Unit 3 What Will You Do This Summer_Lesson 16 Li Ming\'s Summer Holiday.mp3"', '"000046_Unit 3 What Will You Do This Summer_Lesson 17 Danny\'s Summer Holiday.mp3"', '"000048_Unit 3 What Will You Do This Summer_Lesson 18 Three Kites in the Sky.mp3"', '"000050_Unit 3 What Will You Do This Summer_Again Please.mp3"', '"000054_Unit 4 Li Ming Comes Home_Lesson 19 Buying Gifts.mp3"', '"000058_Unit 4 Li Ming Comes Home_Lesson 20 Looking at Photos.mp3"', '"000060_Unit 4 Li Ming Comes Home_Lesson 21 A Party for Li Ming.mp3"', '"000062_Unit 4 Li Ming Comes Home_Lesson 22 Surprise.mp3"', '"000064_Unit 4 Li Ming Comes Home_Lesson 23 Good-bye.mp3"', '"000066_Unit 4 Li Ming Comes Home_Lesson 24 Danny\'s Surprise Cake.mp3"', '"000068_Unit 4 Li Ming Comes Home_Again Please.mp3"', '"000073_Words in Each Unit_Unit 1.mp3"', '"000073_Words in Each Unit_Unit 2.mp3"', '"000073_Words in Each Unit_Unit 3.mp3"', '"000074_Words in Each Unit_Unit 4.mp3"', '"000080_Reading for Fun_Making the mark.mp3"', '"000084_Reading for Fun_What Will Be,Will Be.mp3"', '"000088_Reading for Fun_The Ugly Duckling.mp3"']
    # audioList = ['"000001_Unit 1 Animals on the Farm_Lesson 1 On the Farm.mp3"', '"000004_Unit 1 Animals on the Farm_Lesson 2 Cats and Dogs.mp3"', '"000006_Unit 1 Animals on the Farm_Lesson 3 Fish and Birds.mp3"', '"000008_Unit 1 Animals on the Farm_Lesson 4 Horses and Rabbits.mp3"', '"000010_Unit 1 Animals on the Farm_Lesson 5 Where.mp3"', '"000012_Unit 1 Animals on the Farm_Lesson 6 Can I Help You.mp3"', '"000014_Unit 1 Animals on the Farm_Again Please.mp3"', '"000017_Unit 2 Animals at the Zoo_Lesson 7 At the Zoo.mp3"', '"000020_Unit 2 Animals at the Zoo_Lesson 8 Tigers and Bears.mp3"', '"000022_Unit 2 Animals at the Zoo_Lesson 9 How Many.mp3"', '"000024_Unit 2 Animals at the Zoo_Lesson 10 Where Do They Live.mp3"', '"000026_Unit 2 Animals at the Zoo_Lesson 11 What Do They Eat.mp3"', '"000028_Unit 2 Animals at the Zoo_Lesson 12 The Clever Monkey.mp3"', '"000030_Unit 2 Animals at the Zoo_Again Please.mp3"', '"000033_Unit 3 Food and Meals_Lesson 13 I\'m Hungry.mp3"', '"000036_Unit 3 Food and Meals_Lesson 14 Would You Like Some Soup.mp3"', '"000038_Unit 3 Food and Meals_Lesson 15 What\'s Your Favourite Food.mp3"', '"000040_Unit 3 Food and Meals_Lesson 16 Breakfast,Lunch and Dinner.mp3"', '"000042_Unit 3 Food and Meals_Lesson 17 What\'s for Breakfast.mp3"', '"000044_Unit 3 Food and Meals_Lesson 18 The Magic Stone.mp3"', '"000046_Unit 3 Food and Meals_Again Please.mp3"', '"000049_Unit 4 Food and Restaurants_Lesson 19 I Like Fruit.mp3"', '"000052_Unit 4 Food and Restaurants_Lesson 20 Hamburgers and Hot Dogs.mp3"', '"000054_Unit 4 Food and Restaurants_Lesson 21 In the Restarant.mp3"', '"000056_Unit 4 Food and Restaurants_Lesson 22 How Much Is It.mp3"', '"000058_Unit 4 Food and Restaurants_Lesson 23 How Much Are They.mp3"', '"000060_Unit 4 Food and Restaurants_Lesson 24 A Little Monkey.mp3"', '"000062_Unit 4 Food and Restaurants_Again Please.mp3"', '"000065_Words in Each Unit_Unit 1.mp3"', '"000065_Words in Each Unit_Unit 2.mp3"', '"000066_Words in Each Unit_Unit 3.mp3"', '"000066_Words in Each Unit_Unit 4.mp3"']

    print(audioList)
    audioUrlList = []
    for i in audioList:
        # i = i.replace(" ","")
        i = i[1:len(i) - 1]
        if "\\u" in i:
            i = i.encode("latin-1").decode("unicode_escape")  # 可能遇到带汉字的音频url,需要转码
        audioUrlList.append("http://thumb.1010pic.com/dmt/diandu/" + bookID + "/mp3/" + i)
    return audioUrlList

if __name__ == '__main__':

    # homeHTML = getHTML("http://www.1010jiajiao.com/dianzi/")
    # # print(homeHTML)
    # versions = getVersionUrlList(homeHTML)   #每个version为一个出版社
#    for i in range(35,38):
#        if i==35:
#            bookIDList = getBookID(getHTML(versions[35]))[3:]
#        else:
#            bookIDList = getBookID(getHTML(versions[i]))
#        downloadOneSetOfBooks(bookIDList)

#    bookID = "75"
#    bookIDList = getBookID(getHTML(versions[14]))
#    bookUrl = "http://www.1010jiajiao.com/diandu/book/"+bookID+".html"
#    bookHTML = getHTML(bookUrl)
#    bookName = re.findall("<title>(.*?)</title>",bookHTML)[0].split("——")[0]
#    tracksDF = getTracksDF(bookHTML)

    downloadOneBook("350")
