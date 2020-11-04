#coding=utf-8

import urllib
from bs4 import BeautifulSoup

#urlopen()得到的是对象
response = urllib.urlopen("http://www.3jy.com")
#html是字符串
html = response.read()
#创建BeautifulSoup对象
soup = BeautifulSoup(html)

#select()得到的对象
yy = soup.select('div[id=content-1]')

#列表里元素是一个对象，<class 'bs4.element.Tag'>，可以继续调用select()
zz = yy[0]


