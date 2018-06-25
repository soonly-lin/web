import re
import requests
import os, stat
import urllib.request
from urllib.parse import urljoin
import  _thread

siteMap = 'http://52.220.15.65:8080/opencms/'
# siteMap = 'http://192.168.24.108:8180/opencms/en/'
siteurl = re.findall(r'http[s]?:\/\/[^\/]+', siteMap)
hostname = ''
if siteurl.__len__() > 0:
    hostname = siteurl[0]


def DownloadFile(fileUrl,html):
    try:
        fileUrl = "/opencms"+fileUrl
        pageUrl = urljoin(siteMap, fileUrl)
        print(pageUrl)
        path = "."+os.path.dirname(fileUrl)
        if not os.path.exists(path):
             os.makedirs(path)
        name = os.path.basename(fileUrl)
        path =path+'/'+ name
        print(name)
        if (name =="index.html"):
            f = open(path, 'w')
            f.write(html)
            f.close()
            readPath(fileUrl)
        # else:
        #     f = open(path, 'wb')
        #     f.write((urllib.request.urlopen(pageUrl)).read())
        #     f.close()

    except Exception as e:
        print("DownloadFile Exception：" + fileUrl)

def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    html = html.decode('UTF-8')
    return html

def getUrl(html):
    reg = r'"\/opencms(.*?)"'
    urlre = re.compile(reg);
    urllist = re.findall(urlre, html)
    return urllist

def getUrl2(html):
    reg = r'\'\/opencms(.*?)\''
    urlre = re.compile(reg);
    urllist = re.findall(urlre, html)
    return urllist

def readPath(fileUrl):
    try:
        fileUrl = urljoin(siteMap, fileUrl)
        print("---------------------------" + fileUrl)
        html = getHtml(fileUrl)
        urllist = getUrl(html)
        for href in urllist:
            href = re.sub('#[^#]+', '', href)
            href = re.sub('\?[^\?]+', '', href)
            if (str(href).endswith("/")):
                href = href + "index.html"

            if href not in hrefSet:
                hrefSet.add(href)
                DownloadFile(href,html)

    except Exception as e:
        print("Exception：" + fileUrl)

srcSet = set()
hrefSet = set()
readPath(siteMap)
