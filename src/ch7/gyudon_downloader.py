import json
import os
import re
import time
from urllib import parse, request as req

PHOTOZOU_API = 'https://api.photozou.jp/rest/search_public.json'
CACHE_DIR = './image/cache'


# 포토주 API 로 이미지 검색하기
def search_photo(keyword, offset=0, limit=100):
    # API 쿼리 조합하기
    keyword_enc = parse.quote_plus(keyword)
    q = 'keyword={0}&offset={1}&limit={2}'.format(keyword_enc, offset, limit)
    url = PHOTOZOU_API + '?' + q
    # 캐시 전용 폴더 만들기
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    cache = CACHE_DIR + '/' + re.sub(r'[^a-zA-Z0-9%#]+', '_', url)
    if os.path.exists(cache):
        return json.load(open(cache, 'r', encoding='utf-8'))
    print('[API] ' + url)
    req.urlretrieve(url, cache)
    time.sleep(1)
    return json.load(open(cache, 'r', encoding='utf-8'))


# 이미지 다운로드하기
def download_thumb(info, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if info is None:
        return
    if 'photo' not in info['info']:
        print('[ERROR] broken info')
        return
    photo_list = info['info']['photo']
    for photo in photo_list:
        title = photo['photo_title']
        photo_id = photo['photo_id']
        url = photo['thumbnail_image_url']
        path = save_dir + '/' + str(photo_id) + '_thumb.jpg'
        if os.path.exists(path):
            continue
        try:
            print('[download]', title, photo_id)
            req.urlretrieve(url, path)
            time.sleep(1)
        except Exception as e:
            print(e)
            print('[ERROR] failed to download url=', url)


# 모두 검색하고 다운로드하기
def download_all(keyword, save_dir, maxphoto=1000):
    offset = 0
    limit = 100
    while True:
        # API 호출
        info = search_photo(keyword, offset=offset, limit=limit)
        if info is None:
            print('[ERROR] no result')
            return
        if ('info' not in info) or ('photo_num' not in info['info']):
            print('[ERROR] broken data')
            return
        photo_num = info['info']['photo_num']
        if photo_num == 0:
            print('photo_num = 0, offset = ', offset)
            return
        # 사진 정보가 포함돼 있으면 다운받기
        print('*** download offset=', offset)
        download_thumb(info, save_dir)
        offset += limit
        if offset >= maxphoto:
            break


if __name__ == '__main__':
    # 모듈로 사용할 수 있게 설정
    download_all('牛丼', './image/gyudon')
