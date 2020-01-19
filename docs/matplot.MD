### 1. 用法

### 2. 运维
#### 1. 中文显示乱码问题
1. 查看字体路径
```py
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import font_manager as fm
print(fm)
# 获取缓存目录
print(fm.get_cachedir())
# 配置文件地址
print(matplotlib.matplotlib_fname())
# /home/duchao/.cache/matplotlib
# /usr/local/lib/python3.5/dist-packages/matplotlib/mpl-data/matplotlibrc
```
2. 下载字体[simhei.ttf](http://www.font5.com.cn/font_download.php?id=151&part=1237887120)
3. 将字体拷贝到 tff 目录下：/usr/local/lib/python3.5/dist-packages/matplotlib/mpl-data/fonts/tff/
4. 删除缓存字体
```bash
rm -rf /home/duchao/.cache/matplotlib
```
5. 修改配置文件
```bash
font.family         : sans-serif 
...
font.sans-serif     : SimHei
...
axes.unicode_minus  : False
```
字库族为 sans-serif，同时添加“SimHei”即宋体到字库族列表中，同时将找到axes.unicode_minus，将True改为False，作用就是解决负号’-‘显示为方块的问题

