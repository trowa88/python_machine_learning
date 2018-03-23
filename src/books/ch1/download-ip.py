# IP 확인 API로 접근해서 결과 출력하기
import urllib.request

url = 'http://api.aoikujira.com/ip/ini'
res = urllib.request.urlopen(url)
data = res.read()

text = data.decode('utf-8')
print(text)
