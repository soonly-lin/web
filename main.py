import re
import os
import urllib.request
from urllib.parse import urlparse
from urllib.parse import urljoin
import time

#siteMap = 'http://127.0.0.1:8080/opencms/sitemap/index.html'
#siteMap = 'http://192.168.24.108:8180/opencms/en/'
siteMap = 'http://52.220.15.65:8080/opencms/sitemap/index.html'

def DownloadFile(pageUrl):
    try:
        print(pageUrl)
        path = urlparse(pageUrl).path
        paths =os.path.dirname(path)

        if not os.path.exists("."+paths):
            os.makedirs("."+paths)
        if str(pageUrl).endswith(".html") == True:
            relpath = os.path.relpath("./opencms/","./"+paths)
            relpath = relpath.replace("\\","/")
            htmls = getHtml(pageUrl)
            html = re.sub(r'"\/opencms' , "\""+relpath , htmls)
            html = re.sub(r'\'\/opencms' , "\'"+relpath , html)
            html = re.sub(r'url\(\/opencms' , "url("+relpath , html)
            html = re.sub(r'\/\"' , "/index.html\"" , html)
            f = open("."+path, 'w',encoding='utf-8')
            f.write(html)
            f.close()

            urllist = getUrl(htmls)
            for href in urllist:
                href = getUrlPath(href)
                pageUrl = urljoin(siteMap, href)
                if (pageUrl not in urlSet and str(pageUrl).endswith(".html") == False):
                    urlSet.add(pageUrl)
                    DownloadFile(pageUrl)

        else:
            urllib.request.urlretrieve(pageUrl, filename="."+path)

    except Exception as e:
        print("DownloadFile Exception：" + pageUrl)


def getHtml(url):
    try:
        page = urllib.request.urlopen(url)
        html = page.read()
        html = html.decode('UTF-8')
        return html
    except Exception as e:
        print("getHtml Exception：" + url)

def getUrl(html):
    reg = r'"\/opencms(.*?)"'
    urlre = re.compile(reg);
    urllist = re.findall(urlre, html)

    regs = r'\'\/opencms(.*?)\''
    urlres = re.compile(regs);
    urllists = re.findall(urlres, html)
    urllist.extend(urllists)

    regs1 = r'url\(\/opencms(.*?)\)'
    urlres1 = re.compile(regs1);
    urllists1 = re.findall(urlres1, html)
    urllist.extend(urllists1)
    return urllist

def getUrlPath(href):
    href = re.sub('#[^#]+', '', href)
    href = re.sub('\?[^\?]+', '', href)
    if (str(href).endswith("/")):
        href = href + "index.html"
    return  '/opencms'+href

def readPath(fileUrl):
    try:
        html = getHtml(fileUrl)
        urllist = getUrl(html)
        for href in urllist:
            href = getUrlPath(href)
            pageUrl = urljoin(fileUrl, href)
            if pageUrl not in urlSet:
                urlSet.add(pageUrl)
                DownloadFile(pageUrl)
    except Exception as e:
        print("Exception：" + fileUrl)

ticks = time.time()
urlSet = set()
readPath(siteMap)
print(time.time()- ticks)
