### 1. sklearn.processing
##### 1. 标准化（Z-Score），或者去除均值和方差缩放(StandardScaler, scale)
公式为：(X-mean)/std  计算时对每个属性/每列分别进行。  
将数据按期属性**(按列进行)**减去其均值，并除以其方差。得到的结果是，对于每个属性/每列来说所有数据都聚集在0附近，方差为1。
```py
# scale
>>> from sklearn import preprocessing
>>> import numpy as np
>>> a = np.array([[ 1., -1.,  2.],
                    [ 2.,  0.,  0.],
                    [ 0.,  1., -1.]])
>>> preprocessing.scale(a)
array([[ 0.        , -1.22474487,  1.33630621],
      [ 1.22474487,  0.        , -0.26726124],
      [-1.22474487,  1.22474487, -1.06904497]])
>>> (a - a.mean(axis=0)) / a.std(axis=0)

# StandardScaler
>>> a
array([[ 1., -1.,  2.],
       [ 2.,  0.,  0.],
       [ 0.,  1., -1.]])
>>> s = preprocessing.StandardScaler().fit(a)
>>> s
StandardScaler(copy=True, with_mean=True, with_std=True)
>>> s.mean_
array([1.        , 0.        , 0.33333333])
# np.sqrt(var_)
>>> s.scale_
array([0.81649658, 0.81649658, 1.24721913])
>>> s.transform(a)
array([[ 0.        , -1.22474487,  1.33630621],
       [ 1.22474487,  0.        , -0.26726124],
       [-1.22474487,  1.22474487, -1.06904497]])
```
##### 2. 将属性缩放到一个指定范围(MinMaxScaler, )
将属性缩放到一个指定的最大和最小值（通常是1-0）之间，这可以通过preprocessing.MinMaxScaler类实现
```py
>>> x
array([[ 1., -1.,  2.],
       [ 2.,  0.,  0.],
       [ 0.,  1., -1.]])
>>> m = preprocessing.MinMaxScaler()
>>> m.fit_transform(x)
array([[0.5       , 0.        , 1.        ],
       [1.        , 0.5       , 0.33333333],
       [0.        , 1.        , 0.        ]])
>>> _std = (x - x.min(axis=0)) / (x.max(axis=0) - x.min(axis=0))
>>> _std
array([[0.5       , 0.        , 1.        ],
       [1.        , 0.5       , 0.33333333],
       [0.        , 1.        , 0.        ]])
# min, max = feature_range
>> _scaled = _std * (max - min) + min

# minmax_scale
>> preprocessing.minmax_scale(x)
```
##### 3. 正则化（Normalization）
正则化的过程是将**每个样本**缩放到单位范数（每个样本的范数为1），如果后面要使用如二次型（点积）或者其它核方法计算两个样本之间的相似性这个方法会很有用。  
该方法主要应用于文本分类和聚类中
```py
>>> x
array([[4, 1, 2, 2],
       [1, 3, 9, 3],
       [5, 7, 5, 1]])
>>> m = preprocessing.Normalizer().fit(x)
>>> m
Normalizer(copy=True, norm='l2')
>>> m.transform(x)
array([[0.8, 0.2, 0.4, 0.4],
       [0.1, 0.3, 0.9, 0.3],
       [0.5, 0.7, 0.5, 0.1]])
>>> n = np.sqrt(np.sum(np.square(x), axis=1)).reshape(3, 1)
>>> n
array([[ 5.],
       [10.],
       [10.]])
>>> x / n
array([[0.8, 0.2, 0.4, 0.4],
       [0.1, 0.3, 0.9, 0.3],
       [0.5, 0.7, 0.5, 0.1]])
preprocessing.normalize(x, norm='l2')
```
##### 4. 二值化–特征的二值化(Binarizer)
特征的二值化是指将数值型的特征数据转换成布尔类型的值。可以使用实用类Binarizer。默认是根据0来二值化，大于0的都标记为1，小于等于0的都标记为0
```py
>>> x
[[1.0, -1.0, 2.0], [2.0, 0.0, 0.0], [0.0, 1.0, -1.0]]
m = Binarizer().fit(X)  # fit does nothing
>>> m
Binarizer(copy=True, threshold=0.0)
>>> m.transform(x)
array([[1., 0., 1.],
       [1., 0., 0.],
       [0., 1., 0.]])
```
##### 5. 类别特征编码(独热编码 OneHotEncoder, LabelEncoder)
```py
>>> x
[['Male', 1], ['Female', 3], ['Female', 2]]
>>> m = preprocessing.OneHotEncoder().fit(x)
>>> m.categories_
[array(['Female', 'Male'], dtype=object), array([1, 2, 3], dtype=object)]
>>> m.transform([['Female', 1], ['Male', 2]]).toarray()
array([[1., 0., 1., 0., 0.],
       [0., 1., 0., 1., 0.]])
m.inverse_transform([[0, 1, 1, 0, 0], [0, 0, 0, 1, 0]])
array([['Male', 1],
       ['Female', 2]], dtype=object)
>>> m.inverse_transform([[0, 1, 1, 0, 0], [1, 1, 0, 1, 0]])
array([['Male', 1],
       ['Female', 2]], dtype=object)
>>> m.inverse_transform([[0, 1, 1, 0, 0], [1, 0, 0, 1, 0]])
array([['Male', 1],
       ['Female', 2]], dtype=object)
####################################
>>> x= [1, 2, 2, 6]
>>> m = preprocessing.LabelEncoder()
>>> m.fit_transform(x)
array([0, 1, 1, 2])
>>> m.classes_
array([1, 2, 6])
>>> m.inverse_transform([2, 1, 1])
array([6, 2, 2])
```
##### 6. 弥补缺失数据(impute.SimpleImpute)
```py
>>> from sklearn import impute
>>> x = [[1, 2], [np.nan, 3], [7, 6]]
# missing_valuesnumber, string, np.nan (default) or None
# strategystring, default=’mean’ | “median” | “most_frequent” |  “constant”
>>> m = impute.SimpleImputer(missing_values=np.nan, strategy='mean')
>>> m.fit_transform(x)
array([[1., 2.],
       [4., 3.],
       [7., 6.]])
```
##### 7. 生成多项式特征 PolynomialFeatures
PolynomialFeatures(degree=2, interaction_only=False, include_bias=True, order='C')  
[a, b], the degree-2 polynomial features are [1, a, b, a^2, ab, b^2]
```py
>>> x = np.arange(6).reshape(3, 2)
>>> m = preprocessing.PolynomialFeatures()
>>> m.fit_transform(x)
array([[ 1.,  0.,  1.,  0.,  0.,  1.],
       [ 1.,  2.,  3.,  4.,  6.,  9.],
       [ 1.,  4.,  5., 16., 20., 25.]])
>>> m = preprocessing.PolynomialFeatures(degree=2, interaction_only=True)
>>> m.fit_transform(x)
array([[ 1.,  0.,  1.,  0.],
       [ 1.,  2.,  3.,  6.],
       [ 1.,  4.,  5., 20.]])
>>> m = preprocessing.PolynomialFeatures(include_bias=False)
>>> m.fit_transform(x)
array([[ 0.,  1.,  0.,  0.,  1.],
       [ 2.,  3.,  4.,  6.,  9.],
       [ 4.,  5., 16., 20., 25.]])
```


### 2.

### 3.
