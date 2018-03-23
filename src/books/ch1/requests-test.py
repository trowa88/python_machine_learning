import requests

r = requests.get('http://api.aoikujira.com/time/get.php')

text = r.text
print(text)

bin_content = r.content
print(bin_content)
