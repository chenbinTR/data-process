# coding=utf-8
import urllib.request
import urllib3


def getHtml(url):
    page = urllib.request.urlopen(url)
    htmlsss = page.read()
    return htmlsss


html = getHtml("http://www.aihuhua.com/hua/")

print(html)
