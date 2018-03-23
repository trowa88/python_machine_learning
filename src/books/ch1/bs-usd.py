from urllib import request as req

from bs4 import BeautifulSoup

url = 'http://info.finance.naver.com/marketindex'
res = req.urlopen(url)

soup = BeautifulSoup(res, 'html.parser')

price = soup.select_one('div.head_info > span.value').string
print('usd/krw = ', price)
