import json

import matplotlib.pyplot as plt
import pandas as pd

with open('./lang/freq.json', 'r', encoding='utf-8') as fp:
    freq = json.load(fp)

# 언어마다 계산하기
lang_dic = {}
for i, lbl in enumerate(freq[0]['labels']):
    fq = freq[0]['freq_list'][i]
    if not (lbl in lang_dic):
        lang_dic[lbl] = fq
        continue
    for idx, v in enumerate(fq):
        lang_dic[lbl][idx] = (lang_dic[lbl][idx] + v) / 2

# Pandas 의 DataFrame 에 데이터 넣기
asc_list = [[chr(n) for n in range(97, 97+26)]]
df = pd.DataFrame(lang_dic, index=asc_list)

# 그래프 그리기
plt.style.use('ggplot')
df.plot(kind='bar', subplots=True, ylim=(0, 0.15))
plt.savefig('lang_plot.png')
