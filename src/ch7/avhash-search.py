# image download url : http://www.vision.caltech.edu/Image_Datasets/Caltech101/Caltech101.html#Download
import os
import re

import numpy as np
from PIL import Image

search_dir = './image/101_ObjectCategories'
cache_dir = './image/cache_avhash'

if not os.path.exists(cache_dir):
    os.mkdir(cache_dir)


# 이미지 데이터를 Average Hash 로 변환하기
def average_hash(f_name, size=16):
    f_name2 = f_name[len(search_dir):]
    # 이미지 캐시하기
    cache_file = cache_dir + '/' + f_name2.replace('/', '_') + '.csv'
    if not os.path.exists(cache_file):
        img = Image.open(f_name)
        img = img.convert('L').resize((size, size), Image.ANTIALIAS)
        pixels = np.array(img.getdata()).reshape((size, size))
        avg = pixels.mean()
        px = 1 * (pixels > avg)
        np.savetxt(cache_file, px, fmt='%.0f', delimiter=',')
    else:
        px = np.loadtxt(cache_file, delimiter=',')
    return px


# 해밍 거리 구하기
def hamming_dist(a, b):
    aa = a.reshape(1, -1)  # 1차원 배열로 변환
    ab = b.reshape(1, -1)
    dist = (aa != ab).sum()
    return dist


# 모든 폴더에 처리 적용하기
def enum_all_files(path):
    for root, dirs, files in os.walk(path):
        for fi in files:
            f_name = os.path.join(root, fi)
            if re.search(r'\.(jpg|jpeg|png)$', f_name):
                yield f_name


# 이미지 찾기
def find_image(f_name, rate):
    src = average_hash(f_name)
    for f_name_ in enum_all_files(search_dir):
        dst = average_hash(f_name_)
        diff_r = hamming_dist(src, dst) / 256
        # print('[check] ', f_name_)
        if diff_r < rate:
            yield (diff_r, f_name_)


# 찾기
src_file = search_dir + '/chair/image_0016.jpg'
html = ''
sim = list(find_image(src_file, 0.25))
sim = sorted(sim, key=lambda x: x[0])
for r, f in sim:
    print(r, '>', f)
    s = '<div style="float: left;"><h3>[ 차이 :' + str(r) + '-' + \
        os.path.basename(f) + ']</h3>' + \
        '<p><a href="' + f + '"><img src="' + f + '" width=400>' + \
        '</a></p></div>'
    html += s

# HTML 로 출력하기
html = '''
<html>
<head>
  <meta charset="UTF-8">
</head>
<body>
<p>
  <img src="{0}" alt="" width="400" />
</p>{1}
</body>
</html>
'''.format(src_file, html)

with open('./avhash-search-output.html', 'w', encoding='utf-8') as ff:
    ff.write(html)
print('ok')
