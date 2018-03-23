import re

from bs4 import BeautifulSoup

html = '''
<ul>
  <li><a href="hoge.html">hoge</a></li>
  <li><a href="https://example.com/fuga">fuga*</a></li>
  <li><a href="https://example.com/foo">foo*</a></li>
  <li><a href="http://example.com/aaa">aaa</a></li>
</ul>
'''

soup = BeautifulSoup(html, 'html.parser')
li = soup.find_all(href=re.compile(r'^https://'))
for e in li:
    print(e.attrs['href'])
