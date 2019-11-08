#encoding=utf8
import requests
import sys
import re
import lxml.html
from lxml import etree
from bs4 import BeautifulSoup

text = '''
<meta name="viewport" content="user-scalable=no,viewport-fit=cover">
<meta http-equiv="Pragma" content="no-cache">
<link rel="dns-prefetch" href="//s1.hdslb.com">
<link rel="dns-prefetch" href="//i0.hdslb.com">
<link rel="dns-prefetch" href="//i1.hdslb.com">
<link rel="dns-prefetch" href="//i2.hdslb.com">
<link rel="dns-prefetch" href="//api.bilibili.com">
<link rel="dns-prefetch" href="//static.hdslb.com">
<link rel="preconnect" href="https://www.bilibili.com">
<link rel="preconnect" href="https://api.bilibili.com">

<title>【巅峰之智2】抢椅子篇（中）_综合_动画_哔哩哔哩</title>
<meta itemprop="name" content="【巅峰之智2】抢椅子篇（中）" />
<meta itemprop="image" content="https://i2.hdslb.com/bfs/archive/a53bb3925b0b9ba8fc4995f3261c67ac486019c0.jpg@400w_300h.jpg" />
<meta name="description" itemprop="description" content="本期素材：《欺诈游戏》 来补充一下讲解的设定，免得大家误解。主线的剧情是，为了拯救死亡的青梅竹马，小饭接受神明的考验。灵魂附身在不同的漫画主角身上通关不同的游戏，一旦全部成功，就能用自己的命换回美羽的命。所以每期漫画主角不一样你们就当做是小饭魂穿就行了。这样我就可以挑出不同漫画最精彩的内容给大家，让大家感受到不一样的解说体验，同时对喜欢漫画的朋友可以自行选择补番，感谢大家一直以来的支持。" />
<meta name="title" content="【巅峰之智2】抢椅子篇（中）">
<meta name="keywords" content="哔哩哔哩,bilibili,在线视频,弹幕视频,动画,综合,小饭中年事件簿" />
<meta name="author" content="小饭中年事件簿" />

'''


type = sys.getfilesystemencoding()
s = requests.session()
url = ''
proxie = {
        'http' : 'http://49.4.14.49'
    }
url = 'https://www.bilibili.com/video/av74347033/?spm_id_from=333.334.b_63686965665f7265636f6d6d656e64.20'
header = {
'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
 }
response = s.get(url,headers = header,verify=False,proxies = proxie,timeout = 20)
#print(response.text)
html1 = response.text
soup = BeautifulSoup(html1,'lxml')
description = soup.find(attrs={"name": "description"})['content']
print(description)