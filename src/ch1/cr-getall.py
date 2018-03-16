import os
import re
from os import makedirs
from urllib.parse import urljoin, urlparse
from urllib.request import urlretrieve

import time
from bs4 import BeautifulSoup

# 이미 처리한 파일인지 확인
proc_files = {}


def enum_links(html, base):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select('link[rel="stylesheet"]')
    links += soup.select('a[href]')
    result = []
    for a in links:
        href = a.attrs['href']
        url = urljoin(base, href)
        result.append(url)
    return result


def download_file(url):
    o = urlparse(url)
    save_path = './' + o.netloc + o.path
    if re.search(r'/$', save_path):
        save_path += 'index.html'
    save_dir = os.path.dirname(save_path)
    if os.path.exists(save_path):
        return save_path
    if not os.path.exists(save_dir):
        print('mkdir=', save_dir)
        makedirs(save_dir)

    try:
        print('download=', url)
        urlretrieve(url, save_path)
        time.sleep(1)
        return save_path
    except Exception as e:
        print('다운 실패: ', url)
        print(e)
        return None


def analyze_html(url, root_url):
    save_path = download_file(url)
    if save_path is None:
        return
    if save_path in proc_files:
        return
    proc_files[save_path] = True
    print('analyze_html=', url)
    html = open(save_path, 'r', encoding='utf-8').read()
    links = enum_links(html, url)

    for link_url in links:
        if link_url.find(root_url) != 0:
            if not re.search(r'.css$', link_url):
                continue
        if re.search(r'.(html|htm)$', link_url):
            analyze_html(link_url, root_url)
            continue
        download_file(link_url)


if __name__ == '__main__':
    url = 'https://docs.python.org/3.6/library/'
    analyze_html(url, url)
