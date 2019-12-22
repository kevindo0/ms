#### 1. 如何声明包含多列主键的表类
```python
# 如果列的声明顺序与它们在主键中的顺序相同
class User(Base):
    field1 = Column(Integer, primary_key=True)
    field2 = Column(Integer, primary_key=True)
# 否则在__table_args__中声明
from sqlalchemy import PrimaryKeyConstraint
class User(Base):
    field1 = Column(Integer)
    field2 = Column(Integer)
    __table_args__ = (
        PrimaryKeyConstraint('field2', 'field1'),
    )
```
#### 2. merge 和 update的区别
使用merge方法，如果数据库中有该记录，则更新该记录，如果不存在该记录，则进行insert操作。  
使用update的话，会无条件执行update。  
也就是说如果数据库中有该记录的话，merge和update是一样的。  
但是如果数据库中没有该记录，使用merge执行insert，不会报错，而使用update会报错。
#### 3. default 与 server_default 的区别
Column('foo', Integer, server_default="50")  
其中default 与 server_default 的区别?

* default是插入时sqlalchemy自己干.
* server_default是写在sql创建时让db干的.
