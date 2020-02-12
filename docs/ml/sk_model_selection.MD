### 1. train_test_split()
* shuffle: boolean, optional (default=True)
* test_size: float, int or None, optional (default=None)
* train_size: float, int, or None, (default=None)

```py
from sklearn.model_selection import train_test_split
X, y = np.arange(10).reshape((5, 2)), range(5)
# x: array([[0, 1],[2, 3],[4, 5],[6, 7],[8, 9]])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
# [array([[4, 5],[0, 1],[6, 7]]), array([[2, 3],[8, 9]]), [2, 0, 3], [1, 4]]
```

### 2. cross_val_score(estimator, X, y=None, groups=None, scoring=None, cv=None, n_jobs=None, verbose=0, fit_params=None, pre_dispatch='2*n_jobs', error_score=nan)
cv=k  
作用：验证某个模型在某个训练集上的稳定性，输出k个预测精度。  
把初始训练样本分成k份，其中（k-1）份被用作训练集，剩下一份被用作评估集，这样一共可以对分类器做k次训练，并且得到k个训练结果。
```py
from sklearn import datasets, linear_model
from sklearn import model_selection
diabetes = datasets.load_diabetes()
x = diabetes.data[:150]
y = diabetes.target[:150]
m = linear_model.Lasso()
model_selection.cross_val_score(m, x, y, cv=4)
# array([ 0.3392459 ,  0.12286347,  0.16482017, -0.04610521])
```
