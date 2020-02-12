#### 1. 删除pandas.DataFrame 中包含NaN的行或列
```py
# 判断值value是否为NaN
np.isnan(value
value is np.nan
# 删除NaN所在行
data.dropna(axis=0,how='all')
# 删除表中含有任何NaN的行
data.dropna(axis=0,how='any')
# 删除表中全部为NaN的列
data.dropna(axis=1, how='all')
# 删除表中含有任何NaN的列
data.dropna(axis=1, how='any')
```
