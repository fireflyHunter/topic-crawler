#encoding=utf8
import requests
import sys
from bs4 import BeautifulSoup

type = sys.getfilesystemencoding()
s = requests.session()
url = ''
proxie = {
//这里要变化 ip地址 
        'http' : 'http://187.87.76.251:3128'
    }
url = 'https://www.bilibili.com/video/av74347033/?spm_id_from=333.334.b_63686965665f7265636f6d6d656e64.20'
header = {
'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
 }
response = s.get(url,headers = header,verify=False,proxies = proxie,timeout = 20)
print(response.text)
