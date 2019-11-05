from crawler.scripts.GetAss import download_title
import os
from sklearn.metrics import jaccard_score
def edit_distance(s1, s2):
    m=len(s1)+1
    n=len(s2)+1

    tbl = {}
    for i in range(m): tbl[i,0]=i
    for j in range(n): tbl[0,j]=j
    for i in range(1, m):
        for j in range(1, n):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            tbl[i,j] = min(tbl[i, j-1]+1, tbl[i-1, j]+1, tbl[i-1, j-1]+cost)

    return tbl[i,j]


def jaccard_similarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    return len(s1.intersection(s2)) / len(s1.union(s2))


def get_all_videos():
    video_path = "../videos/"
    video_files = []
    for root, dirs, files in os.walk(video_path):
        video_files.extend(files)
    return video_files

def get_all_danmu_files():
    """
    :param dir:
    :return: all danmu files in a list
    """
    danmu_path = "../danmus/"

    danmu_files = []
    for root, dirs, files in os.walk(danmu_path):
        danmu_files.extend(files)
    return danmu_files
def select_valid_files():
    danmu_files = get_all_danmu_files()
    video_files = get_all_videos()
    video_avid = [x.split(".")[0] for x in video_files]
    danmu_avid = [x.split(".")[0] for x in danmu_files]
    valid_avid = [x for x in video_avid if x in danmu_avid]
    print("{} videos available".format(len(valid_avid)))
    return valid_avid

def title_list(op):
    valid = select_valid_files()
    lines = []
    for avid in valid:
        title = download_title(avid)
        newline = "{}   {}  0\n".format(avid, title)
        lines.append(newline)
    with open(op, 'w', encoding='utf-8') as out:
        out.writelines(lines)

if __name__ == "__main__":
    title_list("../titles.txt")
