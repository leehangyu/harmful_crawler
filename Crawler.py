# This program was created by Hangyu Lee, KPST
# This program uses multiple processes to speed up crawling
# Send an email for any issues
# Author shunchips@kpst.co.kr
import json


import sys
from urllib.request import urlopen
import os
#from builtins import print

from bs4 import BeautifulSoup
import urllib
from multiprocessing import Process, Pool
import time
import multiprocessing


def get_html_addr(page_number):
    for i in range(90, 150):
        print("Processing cateogry : " + str(i))
        try:
            page_number * 20
            html_page = urllib.request.urlopen(
                "https://www.pornpics.com/getchank2.php?rid=1&cat=" + str(i) + "&limit=20&offset=" + str(
                    page_number), data=None, timeout=3)

            soup = BeautifulSoup(html_page, 'html.parser')
            a = json.loads(str(soup))
        except:

            continue


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

    n = 0
    for value in download_url:
        if( n>3):
            continue
        n +=1
        dd = value.find("a")
        url = dd["href"]
        if url == "/":
            continue
        print("Processing .... " + url )
        # _url = "http://wallpaperswide.com" + url
        b = request_url_addr.split('/')
        a = url.split('/')
        file_name = b[4]+ "-"+a[5]
        mypath = sys.argv[1]
        download_path = os.path.join(mypath, file_name)
        # print(a[2])
        urllib.request.urlretrieve(url, download_path)


Page_Number =1
url_list = []




def main():
    start_time = time.time()
    cpus = multiprocessing.cpu_count()
    print('Number of cpu\'s to process WM: %d' % cpus)
    poolcount = 0
    if len(sys.argv) == 2:
        poolcount = cpus * 3
    if len(sys.argv) == 3:
        poolcount = int(sys.argv[2])
    print('using %d processes for this task' % poolcount)
    html_p = Pool(poolcount)

    data = html_p.map(get_html_addr,[i for i in range(1,40)])
    url_list= []
    z = data
    for item in data:
        print(item)
        if(item):
            for z in item:
                if not z in url_list:

                    url_list.append(z)
                else:
                    print("중복된 카테고리 명  : " + z)

    html_p.close()
    html_p.join()

    urls =""

    download_p = Pool(poolcount)


    download_url = download_p.map(download_image, url_list)
    #
    download_p.close()
    download_p.join()
    return

if __name__=="__main__":
    main()