# -*- coding: utf-8 -*-

import urllib
try:
    from urllib.request import Request
except ImportError:
    from urllib2 import Request

try:
    from urllib.parse import parse_qs
except ImportError:
     from urlparse import parse_qs

from urllib import urlencode
from urllib2 import urlopen
import re
import json

#constants
prev_title = '<<'
next_title = '>>'
url_base = 'http://football-plyus.net/'
url_lastmatches = '/football/'
url_menu = 'menuItem'
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Connection': 'keep-alive',
        'Cache-Control':'max-age=0'}


#class for search hits info
class SearchHit:
    _url = ''
    _title = ''
    _image = ''

    def __init__(self, url, title, image):
        self._url = url
        self._title = title
        self._image = image

    def url(self):
        return self._url
    def title(self):
        return self._title
    def image(self):
        return self._image

def getLastMatchesURL():
    return url_lastmatches

def getPrevTitle():
    return prev_title

def getNextTitle():
    return next_title

def getMenuItems():
    request = Request(url_base, headers=headers)
    html = urlopen(request).read().decode('cp1251')

    menus=re.compile('<a class="dropi angle-down">([^"]+?)</a>').findall(html)

    hits = []
    for i,menu in enumerate(menus):
        hits.append(SearchHit(url=url_menu+str(i),title = menus[i],image=''))

    return hits

def openMenu(url):
    request = None

    if (url.startswith(url_menu)):
        request = Request(url_base, headers=headers)
        url = url[len(url_menu):]
    else:
        request = Request(url_base + url, headers=headers)

    html = urlopen(request).read().decode('cp1251')

    menu_blocks=re.compile('<ul class="sub_nav">([\S\s]+?)</ul>').findall(html)
    menu_block = menu_blocks[int(url)]

    menus=re.compile('href="([^"]+?)">').findall(menu_block)
    titles=re.compile('">([^"]+?)</a>').findall(menu_block)

    hits = []
    for i,menu in enumerate(menus):
        hits.append(SearchHit(url=menus[i],title = titles[i],image=''))

    return hits

def openLeague(url):
    request = Request(url_base+url, headers=headers)

    html = urlopen(request).read().decode('cp1251')

    matches=re.compile('<article class="shortstory news1 cf">([\S\s]+?)</article>').findall(html)

    hits = []
    for match in matches:
        pic = re.compile('background-image:url\(([\S\s]+?)\);').findall(match)[0]
        href = re.compile('<a href="([^"]+?)"').findall(match)[0]
        title = re.compile('<a href="[^"]+?">([^"]+?)</a>').findall(match)[0] 

        hits.append(SearchHit(url=href,title = title,image=pic))

    #now fetch prev and next page URLs (if any)
    prev = re.compile('<div class="prev"><a href="([^"]+?)">').findall(html)
    next = re.compile('<div class="next"><a href="([^"]+?)">').findall(html)

    if len(prev) > 0:
        hits.append(SearchHit(url=prev[0],title = getPrevTitle(),image=''))

    if len(next) > 0:
        hits.append(SearchHit(url=next[0],title = getNextTitle(),image=''))

    return hits

def openMatch(url):
    request = Request(url, headers=headers)

    html = urlopen(request).read().decode('cp1251')

    match_data=re.compile('Playerjs\(([\S\s]+?)\);').findall(html)
    print(match_data)
    pics = re.compile('<meta property="og:image" content="([^"]+?)"').findall(html)
    match_data=re.compile('"file":"[\[HD\]]{0,4}([^"]+?)"').findall(match_data[0])

    hits = []
    for i,dt in enumerate(match_data):
        hits.append(SearchHit(url=match_data[i],title = str(i+1)+u' half',image=pics[0]))

    return hits
