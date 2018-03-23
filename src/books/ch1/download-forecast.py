from urllib import request, parse

API = 'http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp'

values = {
    'stnId': '108'
}
params = parse.urlencode(values)
url = API + '?' + params
print('url=', url)

data = request.urlopen(url).read()
text = data.decode('utf-8')
print(text)
