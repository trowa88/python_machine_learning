from urllib import request as req

from bs4 import BeautifulSoup

url = 'http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp'

res = req.urlopen(url)
soup = BeautifulSoup(res, 'html.parser')

title = soup.find('title').string
wf = soup.find('wf').string
print(title)
print(wf)
