# This program was created by Hangyu Lee, KPST
# This program uses multiple processes to speed up crawling
# Send an email for any issues
# Author shunchips@kpst.co.kr
import json
from json import decoder

import sys
from urllib.request import urlopen
import os
#from builtins import print


from bs4 import BeautifulSoup
import urllib
from multiprocessing import Process, Pool
import time
import multiprocessing
from itertools import product

def get_html_addr(page_number, i):
    page_number = page_number * 20
    print("Processing cateogry : " + str(i) + " page number : "+ str(page_number))

    try:
        html_page = urllib.request.urlopen(
            "https://www.pornpics.com/getchank2.php?rid=1&cat=" + str(i) + "&limit=20&offset=" + str(
                page_number), data=None, timeout=3)
        soup = BeautifulSoup(html_page, 'html.parser')
        a = json.loads(str(soup))
    except decoder.JSONDecodeError as e:
        print("ERROR CODE" + str(e))
        # print("Category" +str(i) + "ERROR! message :" + e)

        return


    output = []

    for data in a:
            # print(data['g_url'])
        output.append(data['g_url'])

    return output


def download_image(request_url_addr):
    try:
        html_page = urllib.request.urlopen(request_url_addr, data=None,timeout=5)
        soup = BeautifulSoup(html_page, 'html.parser')
    except:
        print("what")
        return

    download_url = list(soup.findAll("li", {'class' : 'thumbwook'}))
    # print(download_url["href"])

    for value in download_url:

        dd = value.find("a")
        url = dd["href"]
        if url == "/":
            continue

        # _url = "http://wallpaperswide.com" + url
        b = request_url_addr.split('/')
        a = url.split('/')
        file_name = b[4]+ "-"+a[5]
        print("Processing url :" + url + "file name : " + file_name)
        mypath = "C:/Users/sunci/Desktop/crawling/crawler-for-wallpaperswide/d"
        download_path = os.path.join(mypath, file_name)
        # print(a[2])
        urllib.request.urlretrieve(url, download_path)


Page_Number =1
url_list = []




def main():
    start_time = time.time()
    cpus = multiprocessing.cpu_count()
    if(len(sys.argv) != 4):
        print("사용법 : arg1 : 저장할 폴더위치 arg2 : 카테고리시작번호 arg3 : 카테고리 끝번호 arg4 : 사용할 cpu 개수(디폴트 20) ")
        print("예시 : C:/Users/sunci/Desktop/example 2 5")
        print("카테고리 175번까지있습니다.")
        return
    print('Number of cpu\'s to process WM: %d' % cpus)
    if(len(sys.argv) <5):
        poolcount = 20
    else :
        poolcount = int(sys.argv[4])

    print('using %d processes for this task' % poolcount)
    html_p = Pool(poolcount)

    data = html_p.starmap(get_html_addr,product([i for i in range(1,40)], [i for i in range(int(sys.argv[2]), int(sys.argv[3]))]))
    print(data)
    html_p.close()
    html_p.join()
    print(len(data))
    url_list= []
    z = data
    for item in data:
        # print(item)
        if(item):
            for z in item:
                if not z in url_list:
                    print(z)
                    url_list.append(z)
                else:
                    print("중복된 카테고리 명  : " + z)
                pass


    print(len(url_list))

    #
    urls =""

    download_p = Pool(poolcount)


    download_url = download_p.map(download_image, url_list)
    #
    download_p.close()
    download_p.join()
    return

if __name__=="__main__":
    main()