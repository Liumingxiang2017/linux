#coding=utf-8
#正则表达式模块
import re
#获取路径模块
import urllib
def getHtml(url):
	page=urllib.urlopen(url)
	html=page.read()
	return html

def getImage(html):
	imglist = re.findall(r'src="(.*?\.(jpg|png))"',html)
	x=0
	for imgurl in imglist:
		print('正在下载 %s'imgurl[0])
		urllib.urlretrieve(imgurl[0],'./downloads/%d.jpg'%x)
		x+=1

html=getHtml("http://douyu.com/directory/game/LOL")
getImage(html)