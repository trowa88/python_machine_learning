import json
import urllib.request as req
import os

url = 'https://api.github.com/repositories'
save_name = 'repo.json'
if not os.path.exists(url):
    req.urlretrieve(url, save_name)

s = open(save_name, 'r', encoding='utf-8').read()
items = json.loads(s)

for item in items:
    print(item['name'] + ' - ' + item['owner']['login'])
