### 1. DataFram
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
#### 2. Indexing, iteration
#### 1. at, iat, loc, iloc
```py
df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], columns=['a', 'b', 'c'])
df.at[1, 'c']   # 6
df.iat[1, 2]    # 6
df.iat[1, 2] = 100
print(df)
#    a  b    c
# 0  1  2    3
# 1  4  5  100
# 2  7  8    9
df.loc[0]
# a    1
# b    2
# c    3
df.loc[[1, 2]]
#    a  b  c
# 1  4  5  6
# 2  7  8  9
df.loc[1, 'c']  # 6
df.loc[[0, 1], ['a']]
#    a
# 0  1
# 1  4
df.loc[lambda df: df['a'] > 1]
#    a  b  c
# 1  4  5  6
# 2  7  8  9
df.iloc[0]
# a    1
# b    2
# c    3
df.iloc[[0]]
#    a  b  c
# 0  1  2  3
df.iloc[0, 1]      #2
```
### 3. Computations
#### 1. DataFrame.diff(self, periods=1, axis=0) 
```py
df = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6],
                    'b': [1, 1, 2, 3, 5, 8],
                    'c': [1, 4, 9, 16, 25, 36]})
df.diff()
#      a    b     c
# 0  NaN  NaN   NaN
# 1  1.0  0.0   3.0
# 2  1.0  1.0   5.0
# 3  1.0  1.0   7.0
# 4  1.0  2.0   9.0
# 5  1.0  3.0  11.0
df.diff(axis=1)
#     a    b     c
# 0 NaN  0.0   0.0
# 1 NaN -1.0   3.0
# 2 NaN -1.0   7.0
# 3 NaN -1.0  13.0
# 4 NaN  0.0  20.0
# 5 NaN  2.0  28.0
```
#### 2. DataFrame.cumsum(self, axis=None, skipna=True, \*args, \*\*kwargs)
计算沿轴的累计和
```py
df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], columns=['a', 'b', 'c'])
df.cumsum()
#     a   b   c
# 0   1   2   3
# 1   5   7   9
# 2  12  15  18
df.cumsum(axis=1)
#    a   b   c
# 0  1   3   6
# 1  4   9  15
# 2  7  15  24
```
### 4. other
#### 1. DataFrame.assign(self, \*\*kwargs) → DataFrame
将新列重新分配给DataFrame
```py
df = pd.DataFrame([[1, 2, 3], [4, 5, 6]], columns=['a', 'b', 'c'])
df.assign(s=[60, 70])
#    a  b  c   s
# 0  1  2  3  60
# 1  4  5  6  70
df.assign(s = lambda x: x.b + 100)
#    a  b  c    s
# 0  1  2  3  102
# 1  4  5  6  105
df.assign(s = lambda x:x.b + 100, p = lambda x: x['s'] + 200)
#    a  b  c    s    p
# 0  1  2  3  102  302
# 1  4  5  6  105  305
```
#### 2. DataFrame.mask(self, cond, other=nan, inplace=False, axis=None, level=None, errors='raise', try_cast=False)
Replace values where the condition is True.
```py
df = pd.DataFrame([[1, 2, 3], [4, 5, 6]], columns=['a', 'b', 'c'])
df.mask(df % 2 == 0, -9)
#    a  b  c
# 0  1 -9  3
# 1 -9  5 -9
df.mask(df % 2 == 0, -df)
#    a  b  c
# 0  1 -2  3
# 1 -4  5 -6
```
#### 3. DataFrame.where(self, cond, other=nan, inplace=False, axis=None, level=None, errors='raise', try_cast=False)
Replace values where the condition is False.
```py
df.where(df % 3 == 2, -9)
#    a  b  c
# 0 -9  2 -9
# 1 -9  5 -9
df.where(df % 3 == 2, -df)
#    a  b  c
# 0 -1  2 -3
# 1 -4  5 -6
```

