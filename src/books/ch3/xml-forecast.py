import urllib.request as req

import os

from bs4 import BeautifulSoup

url = 'http://www.weather.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=108'
save_name = 'forecast.xml'
if not os.path.exists(save_name):
    req.urlretrieve(url, save_name)

xml = open(save_name, 'r', encoding='utf-8').read()
soup = BeautifulSoup(xml, 'html.parser')

info = {}
for location in soup.find_all('location'):
    name = location.find('city').string
    weather = location.find('wf').string
    if not (weather in info):
        info[weather] = []
    info[weather].append(name)

for weather in info.keys():
    print('+', weather)
    for name in info[weather]:
        print('| - ', name)
