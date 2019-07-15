import csv
import requests
from urllib.parse import urlencode
import re
import os
import json
from hashlib import md5
from multiprocessing.pool import Pool
import time

def read_video(filename):
    try:
        url = []
        with open(filename,'r',encoding='gbk') as csvfile:
            reader = csv.reader(csvfile)
            for reade in reader:
               url.append(reade[0])
            # print(url)
            return url
    except:
        print('error')
        return None

def get_url(url):
    if url:
        headers = {
            'Referer': url,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'X-requested-with': 'XMLHttpRequest'
        }
        params = {
            'feedid':url[-17:],
            'recommendtype':'0',
            'datalvl':'all',
            'format':'json',
            'inCharset':'utf-8',
            'outCharset':'utf-8'
        }
        fin_url = 'https://h5.weishi.qq.com/webapp/json/weishi/WSH5GetPlayPage?' + urlencode(params)
        try:
            r = requests.get(fin_url,headers=headers)
            if r.status_code == 200:
                # print(r.text)
                return r.json()

        except Exception as e:
            print('get_url Error !!!: ',e)

def get_video(json_):
    try:
        if json_.get('data'):
            pararms = re.compile("'video_spec_urls'.*?'url': '(.*?)'")
            result = re.findall(pararms,str(json_))
            return result[0]
            # print(result[0])
        else:
            print("get_video Not Found \'video_spec_urls\'")
            return None
    except:
        return None

def save_to_video(url):
    video_path = 'Video'
    if not os.path.exists(video_path):
        os.mkdir(video_path)
    try:
        videos = requests.get(url)
        if videos.status_code == 200:
            file_path = '{0}{1}{2}.{3}'.format(video_path, os.path.sep, md5(videos.content).hexdigest(), 'mp4')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as file:
                    file.write(videos.content)
                    print('Already Download: {}'.format(file_path))
    except Exception as e:
        print('save_to_video Error :',e)

def main(url):
    save_to_video(get_video(get_url(url)))

if __name__ == '__main__':
    pool = Pool()
    filename = 'movies.csv'
    pool.map(main, read_video(filename))
    time.sleep(1)
    pool.close()
    pool.join()

    # done?