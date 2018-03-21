def n_gram(s, num):
    res = []
    s_len = len(s) - num + 1
    for i in range(s_len):
        ss = s[i:i+num]
        res.append(ss)
    return res


def diff_n_gram(sa, sb, num):
    a = n_gram(sa, num)
    b = n_gram(sb, num)
    r = []
    cnt = 0
    for i in a:
        for j in b:
            if i == j:
                cnt += 1
                r.append(i)
    return cnt / len(a), r


a_t = '오늘 강남에서 맛있는 스파게티를 먹었다.'
b_t = '강남에서 먹었던 오늘의 스파게티는 맛있었다.'
# 2-gram
r2, word2 = diff_n_gram(a_t, b_t, 2)
print('2-gram:', r2, word2)
# 3-gram
r3, word3 = diff_n_gram(a_t, b_t, 3)
print('3-gram:', r3, word3)
