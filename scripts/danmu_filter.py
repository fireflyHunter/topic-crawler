import os
default_encoding = 'utf-8'
import jieba
import re
import matplotlib.pyplot as plt

from collections import OrderedDict
from zhon.hanzi import punctuation
from string import punctuation as eng_punctuation
from crawler.scripts.GetAss import download_title
from crawler.scripts.video_download import download_vid_cover
punctuation += eng_punctuation
punctuation += '丨'
from crawler.scripts.utils import *
import tqdm
MIN_DANMU_LEN = 2
MAX_DANMU_LEN = 50
TOP_N = 50
DIST_THRESHOLD = 0.6
DANMU_PATH="../danmus/"
CLEAN_DANMU_PATH="../danmu_clean/"
STOP_WORDS = ""
MAX_SENT = 50
def get_all_danmu_files(dir=DANMU_PATH):
    """
    :param dir:
    :return: all danmu files in a list
    """
    danmu_files = []
    for root, dirs, files in os.walk(dir):
        danmu_files.extend(files)
    return danmu_files
    
    
def danmu_read_and_clean(file, rmPunc = True):
    """
    :param file:
    :return: plain danmu list, clean it a little
    """
    file = os.path.join(DANMU_PATH,file)
    danmu_list = []
    with open(file,'r',encoding='utf-8') as f:
        for line in f.readlines():
            if line.startswith("Dialogue"):
                danmu = line.split("}")[-1]
                if rmPunc:
                    danmu = remove_punc(danmu)
                if len(danmu) < MIN_DANMU_LEN or len(danmu) > MAX_DANMU_LEN:
                    continue
                danmu_list.append(danmu)
                
    return danmu_list


def remove_punc(sent):
    """
    :param sent: sentence to be processed
    :return: sentence without punctuation
    """
    sent = sent.replace('\\', '')
    return re.sub(r"[%s]+" %punctuation, "", sent).strip()


def danmu_filter_base(danmu_list):
    """
    
    :param danmu_list: un-processed danmu list
    :return: new list which get rid of duplicate danmu.
    """
    danmu_dict = {}
    for danmu in danmu_list:
        if danmu in danmu_dict.keys():
            danmu_dict[danmu] += 1
        else:
            danmu_dict[danmu] = 1
    
    return list(danmu_dict.keys())


def danmu_filter_2rounds(danmu_list):
    """

    :param danmu_list: un-processed danmu list
    :return: new list which get rid of duplicate danmu. using jaccard similarity for second round filter.
    """
    new_danmu_list = []
    danmu_dict = {}
    for danmu in danmu_list:
        if danmu in danmu_dict.keys():
            danmu_dict[danmu] += 1
        else:
            danmu_dict[danmu] = 0
            
    danmu_dict = sorted(danmu_dict.items(), key=lambda n: n[1], reverse=True)
    
    top_n_list = []
    normal = []
    #non top n list
    
    for popular_danmu in danmu_dict[:TOP_N]:
        top_n_list.append(popular_danmu[0])
    new_danmu_list.extend(top_n_list)

    for normal_danmu in danmu_dict[TOP_N:]:
        normal.append(normal_danmu[0])
    c_n = 0
    for danmu in normal:
        canAppend = True
        for popular_danmu in top_n_list:
            
            dist = 1 - jaccard_similarity(popular_danmu, danmu)
            
            
            if dist < DIST_THRESHOLD:
                # means 2 sentences are about the same stuff.
                canAppend = False
                c_n+=1
                # if dist <0.4:
                #     print(popular_danmu + '\n' + danmu + '\n#############')

        if canAppend:
            new_danmu_list.append(danmu)
    ordered_new_list = [x for x in danmu_list if x in new_danmu_list]
    ordered_new_list = list(OrderedDict.fromkeys(ordered_new_list))
    return ordered_new_list
    
def write_danmu(danmu_list, avid, title, path=CLEAN_DANMU_PATH):
    """
    write cleaned and filtered danmu into text file with title
    """
    # danmu_list = ["0    "+x+'\n' for x in danmu_list]
    danmu_list = [x + '\n' for x in danmu_list]
    new_file_name = avid+".cl"
    new_file_path = os.path.join(path, avid)
    with open(new_file_path, 'w', encoding='utf-8') as output:
        output.write(title+'\n'+'\n')
        output.writelines(danmu_list)
    
def fenci(danmu_list):
    """
    :param danmu_list: list of sent to be processed
    :return: fenci_list: list of sent with spaces.
    """
    fenci_list = []
    for sent in danmu_list:
        fenci_sent = list(jieba.cut(sent))
        fenci_sent = [x for x in fenci_sent if x not in STOP_WORDS]
        fenci_line = " ".join(fenci_sent)
        fenci_list.append(fenci_line)
    return fenci_list


def process_sample():
    danmu_files = get_all_danmu_files()
    output_path = "../annotate_sample"

    for index, file in enumerate(danmu_files):
        danmu_list = danmu_read_and_clean(file)
        #clean the danmu list
        output_data = []
        avid = file.split('.')[0]
        title = download_title(avid)
        print(title)
        if not title:
            print("{} has no title".format(avid))
            continue
        output_data.append(title+'\n')
        output_file = os.path.join(output_path, avid+'.txt')
        if len(danmu_list) < 10:
            print("{} has less than 10 danmu".format(file))
            continue
        new_danmu_list = danmu_filter_2rounds(danmu_list)
        new_danmu_list = ['0    '+x+'\n' for x in new_danmu_list]
        output_data.extend(new_danmu_list)
        with open(output_file, 'w', encoding='utf-8') as o:
            o.writelines(output_data)
        #filter danmu list to get rid of reduntant content.



def process(output="../word_vecs/fenci_sent_50.txt"):
    danmu_files = get_all_danmu_files()
    fenci_corpus = []
    f_rates = []
    sum_of_danmu = 0
    for index, file in enumerate(danmu_files):
        danmu_list = danmu_read_and_clean(file)
        #clean the danmu list
        if len(danmu_list) < 10:
            print("{} has less than 10 danmu".format(file))
            continue
        new_danmu_list = danmu_filter_2rounds(danmu_list)
        #filter danmu list to get rid of reduntant content.
        fenci_list = fenci(new_danmu_list)
        #fenci
        sentence = [" ".join(x.split()) for x in fenci_list]
        num_sub_sen = len(sentence)//MAX_SENT + 1
        for i in range(num_sub_sen):
            start = i*MAX_SENT
            end = min((i+1)*MAX_SENT, len(sentence)-1)
            sub_sentence = sentence[start:end]
            sub_sentence = " ".join(sub_sentence) + '\n'
            fenci_corpus.extend(sub_sentence)
        # fenci_corpus.extend(sentence)
        # f_r = len(new_danmu_list)/len(danmu_list)
        # f_r = round(1-f_r, 8)
        # f_rates.append(f_r)
        # sum_of_danmu += len(new_danmu_list)
    with open(output,'w',encoding='utf-8') as o:
        o.writelines(fenci_corpus)


    # print("mean filter rate: {}\nnum of videos: {}".format(sum(f_rates)/len(f_rates),len(f_rates)))
    # print("{} danmu in total".format(sum_of_danmu))
def split_train_test(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = f.readlines()
    print("{} sents in total".format(len(data)))
    valid_size = int(len(data)*0.05)
    train, valid = data[valid_size:], data[:valid_size]
    with open(file+'.train', 'w', encoding='utf-8') as t:
        t.writelines(train)
    with open(file+'.valid', 'w', encoding='utf-8') as v:
        v.writelines(valid)
def build_vocab(file, output):
    from itertools import groupby
    tokens_all = []
    vocab = {}
    vocab_list = ['<S>', '</S>', '<UNK>']  
    with open(file,'r',encoding='utf-8') as f:
        for line in f.readlines():
            tokens_all.extend(line.strip().split())
    tokens_all.sort()
    vocab = {k: sum(1 for _ in g) for k, g in groupby(tokens_all)}
    vocab = sorted(vocab.items(), key=lambda x: x[1],reverse=True)
    vocab_list.extend([x[0] for x in vocab if x[1]>5])
    vocab_list = [x+'\n' for x in vocab_list]
    with open(output,'w',encoding='utf-8') as o:
        o.writelines(vocab_list)
    # vocab = {i: tokens_all.count(i) for i in tokens_all}

    
if __name__ == "__main__":
    files = get_all_danmu_files(DANMU_PATH)
    files = files[40:60]
    for file in files:
        vid = file[2:-4]
        download_vid_cover(vid)


    # files = get_all_danmu_files(DANMU_PATH)
    # # files = files[:1975]
    # plt_data = []
    # from tqdm import tqdm
    #
    # for file in tqdm(files):
    #
    #     avid = file.split('.')[0]
    #     file = avid+'.ass'
    #     # title = download_title(avid)
    #     # if not title:
    #     #     continue
    #     danmu_list = danmu_read_and_clean(file, rmPunc=True)
    #     original_len = len(danmu_list)
    #     if original_len <= 300 or original_len >= 3000:
    #         continue
    #     danmu_list = danmu_filter_2rounds(danmu_list)
    #     # danmu_list = set(danmu_list)
    #     # cpcat_rate = 1 - len(danmu_list) / original_len
    #     plt_data.append(len(danmu_list))
    #     # write_danmu(danmu_list,'av30316182', 'test sample')
    #
    #     # danmu_data = []
    #     # for index, sent in enumerate(danmu_list):
    #     #     danmu_data.append(str(index) + " " + sent)
    #     # write_danmu(danmu_data, avid + '.txt', title, path='../danmu_label_test')
    # # print(len(plt_data))
    # print(sum(plt_data)/len(plt_data))
    # plt.hist(plt_data, bins=40, normed=0, facecolor="blue", edgecolor="black", alpha=0.7)
    # plt.xlabel("number of danmu in one video")
    # plt.ylabel("number of videos")
    # plt.title("Number of Danmu")
    # plt.show()

