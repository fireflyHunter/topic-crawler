# this file collects video id from bilibili
from bs4 import BeautifulSoup
import requests
from crawler.scripts.video_download import download_vid
from crawler.scripts.GetAss import download_danmu, download_title, get_views
import re, os, html5lib

#bilibili 生活区
VID_DATA_PATH = '../database/live_v.txt'
VID_OLD_PATH = '../database/live_v.txt.old'
DANMU_DATA_PATH = '../database/live_d.txt'
DANMU_OLD_PATH = '../database/live_d.txt.old'
URL = 'https://www.bilibili.com/ranking/all/160/0/1'
LIFE_URL = 'https://www.bilibili.com/v/life/'
TECH_URL = 'https://www.bilibili.com/v/technology/'



# link example: https://www.bilibili.com/video/av31424981
# vid: av31424981

def parse_url(link):
    vid = None
    if link:
        if len(link) > 2 & (link[:2] == "//"):
            link = link[2:]
        else:
            return None
        if "video/av" in link:
            vid = link.split("/")[-2]
            if len(link) != 34:
                print("exception found: {}".format(link))
    return vid


def read_data(vid):
    if vid:
        OLD_PATH, DATA_PATH = VID_OLD_PATH, VID_DATA_PATH
    else:
        OLD_PATH, DATA_PATH = DANMU_OLD_PATH, DANMU_DATA_PATH
    data = {}
    if not os.path.exists(DATA_PATH):
        print("path not exist")
        return data
    f = open(DATA_PATH, 'r')
    for line in f.readlines():
        line = line.split("/")
        vid = line[0]
        is_d_downloaded = int(line[1])
        data[vid] = is_d_downloaded
    f.close()
    # if os.path.exists(OLD_PATH):
    #     os.remove(OLD_PATH)
    # os.rename(DATA_PATH,OLD_PATH)
    return data
    
    
def write_data(data,vid):
    if vid:
        DATA_PATH = VID_DATA_PATH
    else:
        DATA_PATH = DANMU_DATA_PATH

    lines = []
    for key, value in data.items():
        value = str(value)
        line = "/".join([key,value])
        line += "\n"
        lines.append(line)
    with open(DATA_PATH, 'w') as o:
        o.writelines(lines)


def scan_ranking_list(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    # soup = BeautifulSoup(page.text, 'html5lib')

    new_vid = []
    for tag in soup.find_all("a"):
        link = tag.get("href")
        vid = parse_url(link)
        if vid:
            new_vid.append(vid)
    return new_vid

def scan_with_regx(url):
    page_text = requests.get(url).text
    vid_list = [page_text[m.start() + 8:m.start() + 16] for m in re.finditer('{"aid":"', page_text)]
    avid_list = ['av' + x for x in vid_list]
    return avid_list





def scan_download_vid():
    current_data = read_data(VID_DATA_PATH)
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    for tag in soup.find_all("a"):
        link = tag.get("href")
        vid = parse_url(link)
        if vid:
            if vid in current_data.keys():
                # vid already downloaded
                print("{} already downloaded".format(vid))
                continue
            else:
                status = download_vid(vid)
                if status == -2:
                    print("video {} unable to download".format(vid))
                    continue
                print("{} is downloaded".format(vid))
                current_data[vid] = status
                
    write_data(current_data)
    

def sync_database(vid):
    vid_path = "../videos"
    danmu_path = "../danmus"
    if vid:
        path = vid_path
    else:
        path = danmu_path
    new_data = {}
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            avid = str(name).split('.')[0]
            new_data[avid] = "0"
    
    write_data(new_data,vid)
    return new_data
    
def scan_download_danmu():
    current_data = read_data(DANMU_DATA_PATH)
    new_data = {}
    for key, value in current_data.items():
        value = int(value)
        if value == 0:
            # 0 means danmu needs to be collected
            try:
                status = download_danmu(key)
                new_data[key] = status
            except Exception:
                print("exception in downloading danmu of {}".format(key))

        else:
            # otherwise just keep the record
            new_data[key] = value
    write_data(new_data)

def process():
    life_vid = scan_with_regx(LIFE_URL)
    tech_vid = scan_with_regx(TECH_URL)
    rank_vid = scan_ranking_list(URL)
    all_vid = life_vid + tech_vid + rank_vid
    all_vid = list(set(all_vid))
    print("crawling finished, {} video found".format(len(all_vid)))
    print("scanning local data...")
    current_danmu = read_data(vid=False)
    # print("{} danmu file found".format(len(list(current_danmu.keys()))))

    current_vid = read_data(vid=True)
    # print("{} video file found".format(len(list(current_vid.keys()))))
    vid_to_download = [vid for vid in all_vid if vid not in current_vid]
    danmu_to_download = [danmu for danmu in all_vid if danmu not in current_danmu]
    print("Start downloading {} danmu file and {} vid file".format(len(danmu_to_download),len(vid_to_download)))
    for vid in vid_to_download:
        title = download_title(vid)
        if vid not in current_vid:
            download_vid(vid)
            print("{} video file downloaded {}".format(vid,title))
        else:
            print("{} already has video file {}".format(vid,title))
    for vid in danmu_to_download:
        title = download_title(vid)
        if vid not in current_danmu:
            download_danmu(vid)
            print("{} danmu file downloaded: {}".format(vid, title))
        else:
            print("{} already has danmu file: {}".format(vid, title))
    #
    # for vid in all_vid:
    #     title = download_title(vid)
    #     if vid not in current_danmu:
    #
    #         download_danmu(vid)
    #         print("{} danmu file downloaded: {}".format(vid,title))
    #     else:
    #         print("{} already has danmu file: {}".format(vid,title))
    #     if vid not in current_vid:
    #         download_vid(vid)
    #
    #         print("{} video file downloaded {}".format(vid,title))
    #     else:
    #         print("{} already has video file {}".format(vid,title))



if __name__ == "__main__":
    # sync_database(True)
    # sync_database(False)
    process()
    # sync_database("../videos")
    #