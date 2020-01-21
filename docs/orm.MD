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
s = sess.query(Book).options(load_only("summary", "title")).first()
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
#### 3. orm.Bundles
绑定包可用于查询同一名称空间下的列组。
```python
from sqlalchemy.orm import Bundle
bn = Bundle('mybundle', MyClass.data1, MyClass.data2)
for row in session.query(bn).filter(bn.c.data1 == 'd1'):
    print(row.mybundle.data1, row.mybundle.data2)
```
#### 4. [Baked Queries](https://docs.sqlalchemy.org/en/13/orm/extensions/baked.html)
预查询
```python
from sqlalchemy.ext import baked
from sqlalchemy import bindparam
bakery = baked.bakery()
baked_query = bakery(lambda session: session.query(User))
baked_query += lambda q: q.filter(User.name == bindparam('name'))
baked_query += lambda q: q.order_by(User.id)
baked_query += lambda q: q.filter(User.status == bindparam('status'))
# SELECT user.id AS user_id, user.name AS user_name, user.status AS user_status FROM user WHERE user.name = 'zl'
result = baked_query(sess).params(name=name, status=status).all()
```
#### 5. func
```python
from sqlalchemy import func
# SELECT user.id AS user_id, concat(user.name, user.address) AS pp FROM user LIMIT 1;
a = sess.query(User.id, func.concat(User.name, User.address).label('pp')).first()
print(a._fields)    # ('id', 'pp')
print(a.pp)         # 'lzshanghai'
print(a._asdict())  # {'id': '1', 'pp': 'lzshanghai'}
#   SELECT user.id AS user_id, concat_ws('-', user.name, user.address) AS pp FROM user LIMIT 1;
a = sess.query(User.id, func.concat_ws('-', User.name, User.address).label('pp')).first()
print(a.pp)         # 'lz-shanghai'

# SELECT user.name AS user_name, group_concat(user.id, user.address, user.status) AS group_concat_1 FROM user GROUP BY user.name
sess.query(User.name, func.group_concat(User.id, User.address, User.status)).group_by(User.name).all()
# [('chao', '3xian5,4wuhan6'), ('lz', '1shanghai1'), ('xiao', '2beijing3')]
# SELECT user.name AS user_name, group_concat(concat_ws('-', user.id, user.address, user.status)) AS group_concat_1 FROM user GROUP BY user.name
sess.query(User.name, func.group_concat(func.concat_ws('-', User.id, User.address, User.status))).group_by(User.name).all()
# [('chao', '3-xian-5,4-wuhan-6'), ('lz', '1-shanghai-1'), ('xiao', '2-beijing-3')]

# SELECT user.id AS user_id, user.name AS user_name, user.address AS user_address, user.status AS user_status FROM user WHERE concat_ws(' ', user.name, user.address) LIKE '%sh%'
sess.query(User).filter(func.concat_ws(' ', User.name, User.address).like('%sh%')).all()
```
#### 6. relationship
* backref: 反向引用
* order_by: list中对象的排序依据
* uselist:  关闭一对多关系，即一对一
* secondary: 关联中间表

一对多：
```py
class Grade(Base):
    
    __tablename__ = "grade"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    users = relationship("User", order_by='User.status')
    def __repr__(self):
        return f"<Grade(id:{self.id} name:{self.name})>"

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    status = Column(Integer)
    grade_id = Column(Integer, ForeignKey('grade.id'))
    grade = relationship("Grade", backref='user_of_grade')
    def __repr__(self):
        return f"<User(name:{self.name}, status:{self.status})>"
```
多对多：

1. 想把需要做多对多的模型定义出来
2. 使用sqlalchemy.Table定义一个中间表，中间表一般就是包含两个模型的外建字段，并且把两个外建作为一个复合主键
3. 在需要多对多的模型中任意选一个来定义relationship，绑定三者之间的关系，在使用relationship的时候需要传入secondary=中间表

```py
association_table = Table('association',Base.metadata,
    Column('course_id', Integer, ForeignKey('course.id')),
    Column('student_id', Integer, ForeignKey('student.id'))
)

class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    student = relationship("Student", secondary=association_table, backref='course')

    def __repr__(self):
        return f"<Course(id:{self.id}, name:{self.name})>"

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    def __repr__(self):
        return f"<Student(id:{self.id}, name:{self.name})>"
# 添加数据
s1 = Student(name = 's1')
s2 = Student(name = 's2')
c1 = Course(name = 'c1')
c2 = Course(name = 'c2')
c1.student = [s1, s2]
c2.student = [s1, s2]
session.add(c1)
session.add(c2)
session.commit()
# SELECT student.id AS student_id, student.name AS student_name FROM student WHERE student.name = 's1' LIMIT 1
a = sess.query(Student).filter_by(name='s1').first()
print(a)   # <Student(id:3, name:s1)>
# SELECT course.id AS course_id, course.name AS course_name FROM course, association WHERE 3 = association.student_id AND course.id = association.course_id
b = a.course
print(b)    # [<Course(id:3, name:c1)>, <Course(id:4, name:c2)>]

# SELECT course.id AS course_id, course.name AS course_name FROM course WHERE course.name = 'c2' LIMIT 1
a = sess.query(Course).filter_by(name='c2').first()
# SELECT student.id AS student_id, student.name AS student_name FROM student, association WHERE 4 = association.course_id AND student.id = association.student_id
b = a.student
print(b)    # [<Student(id:3, name:s1)>, <Student(id:4, name:s2)>]
```
[cascade](https://www.cnblogs.com/zhongyehai/p/11816921.html):

1. save-update：默认选项，在添加一条数据的时候，会把其他和次数据关联的数据都添加到数据库中，这种行为就是save-update属性决定的.
2. delete：表示当删除某一个模型中的数据的时候，也删除掉使用relationship和此数据关联的数据
3. delete-orphan：表示当对一个ORM对象解除了父表中的关联对象的时候，自己便会被删除，如果父表的数据被删除，同样自己也会被删除，这个选项只能用在一对多上，不能用在多对多和多对一上，并且使用的时候还需要在子模型的relationship中增加参数：single_parent=True，前提relationship的cascade需有delete属性
4. merge(合并)：默认选项，当在使用sess.merge合并一个对象的时候，会将使用了relationship相关联的对象也进行merge操作
5. expunge：移除操作的时候，会将相关联的对象也进行移除，这个操作只是从session中移除，并不会正则从数据库删除，与session.add
6. all：对 save-update、merge、refresh-expire、expunge、delete 这几种的缩写

```py
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)

    def __repr__(self):
        return f'<User(id:{self.id}, username:{self.username})>'
class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    uid = Column(Integer, ForeignKey('user.id'))
    author = relationship('User', backref='article')

    def __repr__(self):
        return f'<Article(id:{self.id}, title:{self.title}),author:{self.author}>'
user = User(username='aaa')
article = Article(title='title1')
article.author = user
session.add(article)
# INSERT INTO user (username) VALUES ('aa')
# INSERT INTO article (title, uid) VALUES ('title1', 1)
session.commit()

# 将cascade的值设为空，则不会将模型关系映射成功
# 【 author = relationship('User', backref='article', cascade='')】
user = User(username='bbb')
article = Article(title='title2')
article.author = user
session.add(article)
# INSERT INTO article (title, uid) VALUES ('title2', 1)
session.commit()

# *********************************************
# 删除article，此时对应的user信息也会被删除
# 【 author = relationship('User', backref='article', cascade=cascade='save-update,delete')】
user = User(username='aaa')
article = Article(title='title1')
article.author = user
session.add(article)
# INSERT INTO user (username) VALUES ('aaa')
# INSERT INTO article (title, uid) VALUES ('title1', 2)
session.commit()
# SELECT article.id AS article_id, article.title AS article_title, article.uid AS article_uid FROM article LIMIT 1
a = sess.query(Article).first()
print(a)   # <Article(id:3, title:title1),author:<User(id:2, username:aaa)>>
sess.delete(a)
# DELETE FROM article WHERE article.id = 3
# DELETE FROM user WHERE user.id = 2
sess.commit()
# 同理也可以在user表下做同样设置
class User(Base):
    __tablename__ = 'user'
    # ...
    article = relationship('Article', cascade='save-update,delete')
class Article(Base):
    __tablename__ = 'article'
    # ...
    author = relationship('User', cascade='save-update,delete')

# delete-orphan 测试
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    uid = Column(Integer, ForeignKey('user.id'))
    author = relationship('User', backref=backref('article', cascade='save-update,delete,delete-orphan'),
        cascade='save-update,delete', single_parent=True)
user = User(username='aaa')
article = Article(title='title1')
article.author = user
session.add(article)
session.commit()
a = sess.query(User).first()
print(a)
# 将user下的article置为空，则article表中的数据会为空，由于设置了delete-orphan属性，为空的数据会被删除
# SELECT article.id AS article_id, article.title AS article_title, article.uid AS article_uid FROM article WHERE 3 = article.uid
a.article = []
sess.commit()
# *******************************
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    uid = Column(Integer, ForeignKey('user.id'))
    author = relationship('User', backref=backref('article', cascade='save-update,delete,delete-orphan,merge'),
        cascade='save-update,delete', single_parent=True)
user = User(username='aaa')
article = Article(title='title1')
article.author = user
session.add(article)
session.commit()
a = sess.query(User).first()
user = User(id=1, username='bbb')
article = Article(id=1, title='xxxxxx')
user.article.append(article)
sess.merge(user)
sess.commit()
a = User(id=4, username='aa')
b = Article(id=7, title='xxyyy')
# select * from article;
# +----+-----------+-----+
# | id | title     | uid |
# +----+-----------+-----+
# | 7  | xxxxxx111 | 4   |
# | 8  | 222       | 4   |
# | 9  | xxxxx444  | 4   |
# +----+-----------+-----+
a.article.append(b)
# UPDATE article SET title='xxyyy' WHERE article.id = 7
# DELETE FROM article WHERE article.id = 8
# DELETE FROM article WHERE article.id = 9
sess.commit()
# +----+-----------+-----+
# | id | title     | uid |
# +----+-----------+-----+
# | 7  | xxyyy     | 4   |
# +----+-----------+-----+
# **************************
a = User(username='aaa')
b = Article(title='title1')
a.author = b
sess.add(b)
sess.expunge(b)
# INSERT INTO user (username) VALUES ('aaa')
sess.commit()
```
[lazy](https://www.cnblogs.com/zhongyehai/p/11828196.html)

1. select：如果没有调relationship对应的字段，则不会获取多的这一边的数据，一旦调用此属性，则获取所有对应的数据，返回列表
2. immediate: 不管是否调用relationship对应的字段，都会则获取所有对应的数据，返回列表
3. joined: 将relationship对应的字段查找回来的数据，通过join的方式加到主表数据中
4. subquery: 子查询的方式
5. dynamic: 以后通过relationship定义的对应关系获取到的就不是一个列表，而是一个AppenderQuery对象，这种对象既可以添加新数据，也可以跟Query对象一样对数据进行二次过滤

#### 7. ForeignKey()
##### 1. 使用ondelete指定约束， 外建约束有以下几种：
1. RESTRICT：删除父表数据时，如果子表有数据在使用该字段的数据时，会阻止删除（默认为此约束）
2. NO ACTION：在MySQL中，同RESTRICT
3. CASCADE：级联删除，删除父表的某一条数据时，子表中使用该外建的数据也会被删除
4. SET NULL: 父表数据被删除，删除父表的某一条数据时，子表中使用该外建的数据设置为NULL

```python
# CREATE TABLE article (
#     id INTEGER NOT NULL AUTO_INCREMENT, 
#     title VARCHAR(50) NOT NULL, 
#     uid INTEGER, 
#     PRIMARY KEY (id), 
#     FOREIGN KEY(uid) REFERENCES user (id) ON DELETE RESTRICT
# );
uid = Column(Integer, ForeignKey('user.id', ondelete='RESTRICT'))
# CREATE TABLE article (
#         id INTEGER NOT NULL AUTO_INCREMENT, 
#         title VARCHAR(50) NOT NULL, 
#         uid INTEGER, 
#     PRIMARY KEY (id), 
#     FOREIGN KEY(uid) REFERENCES user (id) ON DELETE CASCADE
# );
uid = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
# SET NULL
# FOREIGN KEY(uid) REFERENCES user (id) ON DELETE SET NULL
```
#### 8. 实现排序的三种方式
```py
# 1. order_by：查询的时候使用此方式根据某个字段或模型下的属性进行排序
# SELECT article.id AS article_id, article.title AS article_title, article.uid AS article_uid FROM article ORDER BY article.id
sess.query(Article).order_by(Article.id).all()
# SELECT article.id AS article_id, article.title AS article_title, article.uid AS article_uid FROM article ORDER BY article.id DESC
sess.query(Article).order_by(Article.id.desc()).all()
from sqlalchemy import desc
sess.query(Article).order_by(desc('id')).all()
# 2. 模型定义的时候，指定排序方式
class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    create_time = Column(DateTime, nullable=False, default=datetime.now)

    __mapper_args__ = {
        'order_by': create_time.desc()
    }

    def __repr__(self):
        return f'title: {self.title}、create_time: {self.create_time}'
# SELECT article.id AS article_id, article.title AS article_title, article.create_time AS article_create_time FROM article ORDER BY article.create_time DESC
sess.query(Article).all()
# 3. 一对多的时候，relationship的order_by参数
# 若未在backref中指定排序规则，则会找__mapper_args__下的排序规则
class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    create_time = Column(DateTime, nullable=False, default=datetime.now)
    uid = Column(Integer, ForeignKey('user.id'))
    author = relationship('User', backref=backref('article', order_by=create_time.desc()))
```
#### 9. limit, slice, offset及切片
1. limit：限制每次查询的时候查询数据的条数
2. slice：查一个区间的数据，slice(起，止)
3. offset：限制查找数据的时候过滤掉前面多少条
4. 切片：对query对象切实获取想要的数据

```python
# limit
sess.query(Article).limit(10).all()
# SELECT article.id AS article_id, article.title AS article_title, article.create_time AS article_create_time FROM article LIMIT 2, 9;
sess.query(Article).slice(2, 11).all()
# ELECT article.id AS article_id, article.title AS article_title, article.create_time AS article_create_time FROM article LIMIT 10, 18446744073709551615
sess.query(Article).offset(10).all()
# SELECT article.id AS article_id, article.title AS article_title, article.create_time AS article_create_time FROM article LIMIT 1, 4
sess.query(Article)[1:5]
```
#### 9. group_by 和 having子句
group_by：将数据根据指定的字段进行分组，如：根据年龄 分组，统计每个组的人数  
having：对返回数据进行二次过滤，类似于where，如：根据年龄 分组，统计每个组的人数，然后再删选出年龄大于25的数据
```py
# SELECT user.age AS user_age, count(user.id) as count_1 FROM User GROUP BY user.age
sess.query(User.age, func.count(User.id)).group_by(User.age)
# SELECT user.age AS user_age, count(user.id) as count_1 FROM User GROUP BY user.age having user.age > 25
sess.query(User.age, func.count(User.id)).group_by(User.age).having(User.age > 25)
```
#### 10. join
```py
class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    create_time = Column(DateTime, nullable=False, default=datetime.now)
    uid = Column(Integer, ForeignKey('user.id'))
    author = relationship('User', backref='article')
# INSERT INTO user (username) VALUES ('user2')
# INSERT INTO article (title, create_time, uid) VALUES ('title1', '2020-01-21 17:23:33.868686', 3)
# INSERT INTO article (title, create_time, uid) VALUES ('title2', '2020-01-21 17:23:33.879594', 3)
user2 = User(username='user2')
for x in range(1):
    article = Article(title=f'title{x}')
    article.author = user2
    session.add(article)
session.commit()
# SELECT user.username AS user_username, count(article.id) AS count_1 FROM user INNER JOIN article ON user.id = article.uid GROUP BY user.id
sess.query(User.username, func.count(Article.id)).join(Article, User.id==Article.uid).group_by(User.id).all()
```
#### 11. subquery
```py
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    age = Column(Integer, default=0)
# 查询和user1在用一个城市，且年龄相等的人
# SELECT user.id AS user_id, user.username AS user_username, user.city AS user_city, user.age AS user_age FROM user, (SELECT user.city AS city, user.age AS age1 FROM user WHERE user.username = 'user1') AS anon_1 WHERE user.city = anon_1.city AND user.age = anon_1.age1
stmt = sess.query(User.city.label('city'), User.age.label('age1')).filter(username='user1').subquery()
users = sess.query(User).filter(User.city==stmt.c.city, User.age==stmt.c.age1).all()
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

