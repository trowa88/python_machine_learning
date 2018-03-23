import pandas as pd

tbl = pd.DataFrame({
    'weight': [80.0, 70.4, 65.5, 45.9, 51.2, 72.5],
    'height': [170, 180, 155, 143, 154, 160],
    'type': ['f', 'm', 'm', 'f', 'f', 'm']
})


# 키와 몸무게 정규화
# 최대값과 최소값 구하기
def norm(n_tbl, key):
    c = n_tbl[key]
    v_max = c.max()
    v_min = c.min()
    print(key, '=', v_min, '-', v_max)
    n_tbl[key] = (c - v_min) / (v_max - v_min)


norm(tbl, 'weight')
norm(tbl, 'height')
print(tbl)
