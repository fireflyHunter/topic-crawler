
import os, re, json, click, requests, urllib, urllib3
from contextlib import closing


class bilibili():
    def __init__(self):
        self.infoheaders = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'zh-CN,zh;q=0.9',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
                    }
        self.downheaders = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                        'accept': '*/*',
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'zh-CN,zh;q=0.9',
                        'Referer': 'https://search.bilibili.com/all?keyword='
                    }
        
    def get(self, url, vid, savepath='../videos'):
        Vurlinfos = self._GetVideoInfos(url)
        if not Vurlinfos:
            return -2
        status = self._Download(Vurlinfos, savepath, vid)
        return status
    
    def _Download(self, Vurlinfos, savepath, vid):
        status = -2
        if not os.path.exists(savepath):
            os.mkdir(savepath)
        name = Vurlinfos[1]
        download_url = Vurlinfos[0]
        with closing(requests.get(download_url, headers=self.downheaders, stream=True, verify=False)) as res:
            total_size = int(res.headers['content-length'])
            #compute size in mb
            size = total_size/(1024*1024)
            if size >= 512:
                print("Not downloading video {} because it exceed the limit of 512MB")
                return status
            if res.status_code == 200:
                label = '[FileSize]:%0.2f MB' % (size)
                with click.progressbar(length=total_size, label=label) as progressbar:
                    with open(os.path.join(savepath, str(vid)+'.flv'), "wb") as f:
                        for chunk in res.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                                progressbar.update(1024)
                        status = 0
        
        return status
    
    def _GetVideoInfos(self, url):
        
        res = requests.get(url=url, headers=self.infoheaders)
        pattern = '.__playinfo__=(.*)</script><script>window.__INITIAL_STATE__='
        try:
            re_result = re.findall(pattern, res.text)[0]
        except IndexError:
            return None
        temp = json.loads(re_result)
        # download_url = temp["data"]['durl'][0]['url']
        download_url = temp["data"]['dash']["video"][0]['baseUrl']
        if 'mirrork' in download_url:
            vid = download_url.split('/')[6]
        else:
            vid = download_url.split('/')[7]
            if len(vid) >= 10:
                vid = download_url.split('/')[6]
        Vurlinfos = [download_url, vid]
        return Vurlinfos

def download_vid(vid):
    url = "https://www.bilibili.com/video/{}/".format(vid)
    status =  bilibili().get(url,vid)
    return status
    
def download_vid_cover(vid):


    url = 'https://api.bilibili.com/x/web-interface/view?aid=%s' % (vid,)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
                'Referer': 'https://www.bilibili.com'}  # 竟然是这里的错误


    urllib3.disable_warnings()  #从urllib3中消除警告
    response = requests.get(url, headers=headers, verify=False)  #证书验证设为FALSE

    content = json.loads(response.text)
    # 获取到的是str字符串 需要解析成json数据

    statue_code = content.get('code')
    if statue_code == 0:
        # print()
        r = requests.get(content.get('data').get('pic'))
        with open("../video_covers/{}.jpg".format(vid), "wb") as code:
            code.write(r.content)
    else:
        print('{}不存在'.format(vid))

if __name__ == '__main__':
    download_vid_cover("41504619")
    # url = "https://www.bilibili.com/video/av25961598/"
    # bilibili().get(url)