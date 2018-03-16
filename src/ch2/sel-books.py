from bs4 import BeautifulSoup


def sel(q):
    print(soup.select_one(q).string)


fp = open('books.html', encoding='utf-8')
soup = BeautifulSoup(fp, 'html.parser')

sel('#nu')
sel('li#nu')
sel('ul > li#nu')
sel('#bible #nu')
sel('ul#bible > li#nu')
sel('li[id="nu"]')
sel('li:nth-of-type(4)')

print(soup.select('li')[3].string)
print(soup.find_all('li')[3].string)

fp.close()
