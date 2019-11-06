#encoding=utf8
import requests
import sys
import re
import lxml.html
from lxml import etree
from bs4 import BeautifulSoup

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

html1 = '''
/html/body/div[3]/div/div[1]/div[5]/ul/li[1]
</span></p></div>
<div class="index__position__src-videoPage-videoInfo-">
<a href="/index.html" target="_self" class="index__crumb__src-videoPage-videoInfo-">主页</a>
<a href="/channel/1.html" target="_self" class="index__crumb__src-videoPage-videoInfo-">动画</a>
<a href="/channel/27.html" target="_self" class="index__crumb__src-videoPage-videoInfo-">综合</a>av74347033</div>
</div></div></div>
<div class="index__relativeTag__src-videoPage-relativeTag- report-wrap-module" id="tags">
<div class="index__tags__src-videoPage-relativeTag-">
<a href="/tag/1184" target="_self" class="index__tag__src-videoPage-relativeTag-">漫画</a><a href="/tag/530918" target="_self" class="index__tag__src-videoPage-relativeTag-">动漫杂谈</a>
<a href="/tag/70246" target="_self" class="index__tag__src-videoPage-relativeTag-">欺诈游戏</a><a href="/tag/11657551" target="_self" class="index__tag__src-videoPage-relativeTag-">全能打卡挑战</a>
<a href="/tag/1296" target="_self" class="index__tag__src-videoPage-relativeTag-">经典</a><a href="/tag/12038620" target="_self" class="index__tag__src-videoPage-relativeTag-">智斗漫画</a></div></div></div></div><div class="index__operateZone__src-videoPage-operateZone- "><div report-id="favorite" 

'''

soup = BeautifulSoup(html1,'lxml')
#print(soup.prettify())
#info = soup.find_all(class_ ='index__tag__src-videoPage-relativeTag-')
#print(info)
info = soup.find_all(attrs={'class': 'index__tag__src-videoPage-relativeTag-'})
print(info)
#s = info.get_text()
#print(s)
print(re.findall(r">(.+?)</a>",info))