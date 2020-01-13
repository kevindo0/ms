### 1. 知识点
#### 1. deferred
This feature is useful when one wants to avoid loading a large text or binary field into memory when it’s not needed.
```python
from sqlalchemy.orm import deferred, defer, undefer
from sqlalchemy import Integer, String, Text, Column
class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    summary = Column(String(2000))
    excerpt = deferred(Column(Text))
# ELECT book.id AS book_id, book.title AS book_title, book.summary AS book_summary FROM book LIMIT 1;
book = sess.query(Book).first()
# SELECT book.excerpt AS book_excerpt FROM book WHERE book.id = 1;
print(book.excerpt)
# SELECT book.excerpt AS book_excerpt, book.id AS book_id, book.title AS book_title FROM book;
sess.query(Book).options(defer('summary'), undefer('excerpt')).all()
from sqlalchemy.orm import load_only
# SELECT book.id AS book_id, book.summary AS book_summary FROM book LIMIT 1;
s = sess.query(Book).options(load_only("summary")).first()
# SELECT book.excerpt AS book_excerpt, book.title AS book_title FROM book WHERE book.id = 1;
s.title
```
#### 2. [Hybrid Attributes](https://docs.sqlalchemy.org/en/13/orm/extensions/hybrid.html?highlight=hybrid_property#sqlalchemy.ext.hybrid.hybrid_property)
```python
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
class Interval(Base):
    __tablename__ = 'interval'
    id = Column(Integer, primary_key=True)
    start = Column(Integer, nullable=False)
    end = Column(Integer, nullable=False)
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def __repr__(self):
        return f'start: {self.start}, end: {self.end}'
        
    @hybrid_property
    def length(self):
        return self.end - self.start

    @length.setter
    def length(self, value):
        self.end = self.start + value

    @length.update_expression
    def length(cls, value):
        return [
            (cls.end, cls.start + value)
        ]

    @hybrid_method
    def contains(self, point):
        return (self.start <= point) & (point <= self.end)

    @hybrid_method
    def intersects(self, other):
        return self.contains(other.start) | self.contains(other.end)
# SELECT `interval`.id AS interval_id, `interval`.start AS interval_start, `interval`.end AS interval_end FROM `interval` WHERE `interval`.end - `interval`.start > 10;
sess.query(Interval).filter(Interval.length > 10)
sess.query(Interval).filter_by(length=5)
# UPDATE `interval` SET end=(`interval`.start + 25)
sess.query(Interval).update({Interval.length: 25}, synchronize_session='fetch')
# UPDATE `interval` SET end=(`interval`.start + 25) WHERE `interval`.end - `interval`.start = 6
sess.query(Interval).filter_by(length=6).update({Interval.length: 25}, synchronize_session='fetch')
```
####3. orm.Bundles
绑定包可用于查询同一名称空间下的列组。
```python
from sqlalchemy.orm import Bundle
bn = Bundle('mybundle', MyClass.data1, MyClass.data2)
for row in session.query(bn).filter(bn.c.data1 == 'd1'):
    print(row.mybundle.data1, row.mybundle.data2)
```

### 2. 问题解决
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

