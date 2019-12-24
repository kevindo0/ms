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

#### 4. scoped_session
* 通过sessionmaker，我们得到一个类，一个能产生session的工厂
* 创建Session是一件比较耗资源的事情
* 使用scoped_session的目的主要是为了线程安全, 类似单例模式，当我们调用使用的时候，会先在Registry里找找之前是否已经创建session了
* 使用了thread local storage技术，使session实现了线程隔离。这样就只能看见本线程的session

#### 5. session.flush()和commit()的区别
1. flush()方法进行清理缓存的操作,执行一系列的SQL语句,但不会提交事务
2. commit()方法会先调用flush()方法,然后提交事务
3. Flush()后只是将Hibernate缓存中的数据提交到数据库,如果这时数据库处在一个事务当中,则数据库将这些SQL语句缓存起来
4. 当Hibernate进行commit时,会告诉数据库,你可以真正提交了,这时数据才会永久保存下来,也就是被持久化了

